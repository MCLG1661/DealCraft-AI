from pathlib import Path
import json
import re
import sys
import unicodedata
from decimal import Decimal, ROUND_HALF_UP


# ============================================================
# DEALCRAFT AI — OPPORTUNITY VALIDATOR
# Version: 2.1
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "DOCS"
CATALOG_PATH = DOCS_DIR / "catalogo-servicos.json"


# ============================================================
# CONSTANTS
# ============================================================

ABSENCE_VALUES = {
    "",
    "nao informado",
    "nao informada",
    "nao informados",
    "nao informadas",
    "nao definido",
    "nao definida",
    "nao definidos",
    "nao definidas",
    "nao aplicavel",
    "nenhum servico foi definido",
    "nenhum servico definido",
}

ABSENCE_PREFIXES = (
    "nao informado",
    "nao informada",
    "nao definido",
    "nao definida",
    "nao existem dados disponiveis",
    "nenhum servico foi definido",
)

MANDATORY_FIELDS = {
    "A1": "Razão social",
    "A2": "Setor",
    "A5": "Contato principal",
    "A6": "Cargo",
    "A7": "E-mail",
    "B1": "Cenário atual",
    "B2": "Principal problema/dor",
    "B3": "Objetivo do projeto",
    "B5": "Urgência",
    "D1": "Serviço(s) recomendado(s)",
    "D2": "Escopo",
    "D3": "Prazo",
    "D4": "Investimento por serviço",
    "E1": "Número da proposta",
    "E2": "Consultor responsável",
    "E3": "E-mail do consultor",
    "E4": "Data de emissão",
}

OPTIONAL_FIELDS = {
    "A3": "Porte",
    "A4": "Localização",
    "A8": "Telefone",
    "B4": "Impacto do problema",
    "B6": "Prazo desejado",
    "B7": "Orçamento disponível",
    "C1": "Decisor",
    "C2": "Influenciadores",
    "C3": "Critérios de decisão",
    "C4": "Concorrentes",
    "C5": "Próximo passo comercial",
    "C6": "Data do próximo contato",
    "D5": "Desconto",
    "D6": "Premissas",
    "D7": "Exclusões",
    "E5": "Idioma",
    "E6": "Observações internas",
}

NARRATIVE_FIELDS = {
    "B1",
    "B2",
    "B3",
    "B4",
    "D2",
    "D6",
    "D7",
    "E6",
}


# ============================================================
# TEXT UTILITIES
# ============================================================

def strip_accents(text):
    if text is None:
        return ""

    normalized = unicodedata.normalize(
        "NFKD",
        str(text)
    )

    return "".join(
        char
        for char in normalized
        if not unicodedata.combining(char)
    )


def normalize(text):
    if text is None:
        return ""

    text = strip_accents(str(text))
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)

    return text.rstrip(".:;")


def clean_value(value):
    if value is None:
        return None

    value = str(value).strip()

    value = re.sub(
        r"^[\-–—•]+\s*",
        "",
        value
    )

    return value.strip()


def is_separator(line):
    return bool(
        re.fullmatch(
            r"[=\-_]{3,}",
            line.strip()
        )
    )


def looks_like_section_title(line):
    return bool(
        re.match(
            r"^\d+\.\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ]",
            line.strip()
        )
    )


# ============================================================
# AVAILABILITY
# ============================================================

def is_available(value):
    if value is None:
        return False

    normalized = normalize(value)

    if not normalized:
        return False

    if normalized in ABSENCE_VALUES:
        return False

    for prefix in ABSENCE_PREFIXES:
        if normalized.startswith(prefix):
            return False

    return True


def narrative_is_available(value):
    if value is None:
        return False

    normalized = normalize(value)

    if not normalized:
        return False

    for prefix in ABSENCE_PREFIXES:
        if normalized.startswith(prefix):
            return False

    return True


def field_available(field_id, value):
    if field_id in NARRATIVE_FIELDS:
        return narrative_is_available(value)

    return is_available(value)


# ============================================================
# GENERIC EXTRACTION
# ============================================================

def extract_after_label(text, label):
    """
    Extrai um valor simples associado a um rótulo.

    Suporta:

    Campo: valor

    e:

    Campo:

    valor
    """

    lines = text.splitlines()
    target = normalize(label)

    for index, raw_line in enumerate(lines):
        line = raw_line.strip()

        if not line or ":" not in line:
            continue

        left, right = line.split(":", 1)

        if normalize(left) != target:
            continue

        right = clean_value(right)

        if right:
            return right

        for next_index in range(
            index + 1,
            len(lines)
        ):
            candidate = lines[
                next_index
            ].strip()

            if not candidate:
                continue

            if is_separator(candidate):
                continue

            if looks_like_section_title(
                candidate
            ):
                return None

            if ":" in candidate:
                possible_label = (
                    candidate.split(
                        ":",
                        1
                    )[0]
                )

                if len(
                    possible_label.split()
                ) <= 8:
                    return None

            return clean_value(candidate)

        return None

    return None


def extract_first_label(text, labels):
    for label in labels:
        value = extract_after_label(
            text,
            label
        )

        if value is not None:
            return value

    return None


def extract_section(
    text,
    start_title,
    end_title=None
):
    pattern_start = re.compile(
        re.escape(start_title),
        re.IGNORECASE
    )

    start_match = pattern_start.search(
        text
    )

    if not start_match:
        return ""

    start = start_match.end()

    if end_title:
        pattern_end = re.compile(
            re.escape(end_title),
            re.IGNORECASE
        )

        end_match = pattern_end.search(
            text,
            start
        )

        end = (
            end_match.start()
            if end_match
            else len(text)
        )
    else:
        end = len(text)

    section = text[
        start:end
    ].strip()

    section = re.sub(
        r"^[=\-_]+\s*",
        "",
        section
    )

    section = re.sub(
        r"\s*[=\-_]+$",
        "",
        section
    )

    return section.strip()


def extract_multiline_after_label(
    text,
    label,
    stop_labels=None,
    section_start=None,
    section_end=None
):
    """
    Extrai um valor associado a um rótulo
    que pode ocupar várias linhas.

    A coleta termina quando encontra:
    - um dos stop_labels;
    - um separador;
    - um novo título numerado de seção.

    Quando section_start é informado,
    a busca fica confinada à seção.
    """

    source = text

    if section_start:
        source = extract_section(
            text,
            section_start,
            section_end
        )

    if not source:
        return None

    stop_targets = {
        normalize(item)
        for item in (
            stop_labels or []
        )
    }

    lines = source.splitlines()
    target = normalize(label)

    for index, raw_line in enumerate(
        lines
    ):
        line = raw_line.strip()

        if not line or ":" not in line:
            continue

        left, right = line.split(
            ":",
            1
        )

        if normalize(left) != target:
            continue

        collected = []

        right = clean_value(right)

        if right:
            collected.append(right)

        for next_index in range(
            index + 1,
            len(lines)
        ):
            candidate = lines[
                next_index
            ].strip()

            if not candidate:
                continue

            if is_separator(candidate):
                break

            if looks_like_section_title(
                candidate
            ):
                break

            if ":" in candidate:
                possible_label, possible_value = (
                    candidate.split(
                        ":",
                        1
                    )
                )

                normalized_label = normalize(
                    possible_label
                )

                if (
                    normalized_label
                    in stop_targets
                ):
                    break

                if (
                    len(
                        possible_label.split()
                    ) <= 8
                    and normalized_label
                    != target
                ):
                    break

                candidate = (
                    possible_value.strip()
                )

            value = clean_value(
                candidate
            )

            if value:
                collected.append(
                    value
                )

        if not collected:
            return None

        return " ".join(
            collected
        )

    return None


# ============================================================
# SPECIFIC EXTRACTION
# ============================================================

def extract_budget(text):
    section = extract_section(
        text,
        "7. ORÇAMENTO",
        "8. PROCESSO DECISÓRIO"
    )

    value = extract_first_label(
        section,
        [
            (
                "Orçamento disponível "
                "informado pelo cliente"
            ),
            "Orçamento disponível",
            "Orçamento",
        ]
    )

    if is_available(value):
        return value

    match = re.search(
        r"R\$\s*[\d\.]+(?:,\d{2})?",
        section
    )

    if match:
        return match.group(0)

    return value


def extract_decision_maker(text):
    return extract_first_label(
        text,
        [
            "Decisor",
            "Decisora",
            "Decisor principal",
            "Decisora principal",
        ]
    )


def extract_solution(text):
    return extract_first_label(
        text,
        [
            "Serviço recomendado",
            "Serviços recomendados",
            (
                "Serviço discutido "
                "com o cliente"
            ),
            "Serviço discutido",
            "Solução recomendada",
        ]
    )


def extract_scope(text):
    return extract_first_label(
        text,
        [
            "Escopo",
            "Escopo preliminar",
            "Escopo proposto",
        ]
    )


def extract_solution_section(text):
    section = extract_section(
        text,
        "9. SOLUÇÃO DISCUTIDA",
        "10. PREMISSAS"
    )

    if section:
        return section

    return extract_section(
        text,
        "9. SOLUÇÃO",
        "10. PREMISSAS"
    )


def extract_solution_deadline(text):
    section = (
        extract_solution_section(
            text
        )
    )

    return extract_first_label(
        section,
        [
            "Prazo proposto",
            "Prazo",
        ]
    )


def extract_solution_investment(text):
    section = (
        extract_solution_section(
            text
        )
    )

    return extract_first_label(
        section,
        [
            "Investimento proposto",
            "Investimento",
        ]
    )


def extract_discount(text):
    section = (
        extract_solution_section(
            text
        )
    )

    return extract_after_label(
        section,
        "Desconto"
    )


def extract_issue_date(text):
    return extract_first_label(
        text,
        [
            "Data de emissão prevista",
            "Data de emissão",
        ]
    )


def extract_next_step(text):
    """
    Extrai C5 preservando texto multilinha.

    Exemplo:

    Próximo passo:

    Apresentação da proposta comercial
    para a Diretora Comercial e para
    o Gerente de Tecnologia.

    Data prevista:

    30/09/2026
    """

    return extract_multiline_after_label(
        text=text,
        label="Próximo passo",
        stop_labels=[
            "Data prevista",
            "Data do próximo contato",
        ],
        section_start=(
            "12. PRÓXIMO PASSO COMERCIAL"
        ),
        section_end=(
            "13. CONTROLE INTERNO"
        ),
    )


# ============================================================
# OPPORTUNITY MODEL
# ============================================================

def extract_opportunity(text):
    opportunity = {}

    opportunity["A1"] = (
        extract_after_label(
            text,
            "Razão social"
        )
    )

    opportunity["A2"] = (
        extract_after_label(
            text,
            "Setor"
        )
    )

    opportunity["A3"] = (
        extract_after_label(
            text,
            "Porte"
        )
    )

    opportunity["A4"] = (
        extract_after_label(
            text,
            "Localização"
        )
    )

    opportunity["A5"] = (
        extract_after_label(
            text,
            "Contato principal"
        )
    )

    opportunity["A6"] = (
        extract_after_label(
            text,
            "Cargo"
        )
    )

    opportunity["A7"] = (
        extract_after_label(
            text,
            "E-mail"
        )
    )

    opportunity["A8"] = (
        extract_after_label(
            text,
            "Telefone"
        )
    )

    opportunity["B1"] = extract_section(
        text,
        "2. CENÁRIO ATUAL",
        "3. PRINCIPAL PROBLEMA"
    )

    opportunity["B2"] = extract_section(
        text,
        "3. PRINCIPAL PROBLEMA",
        "4. OBJETIVO DO PROJETO"
    )

    opportunity["B3"] = extract_section(
        text,
        "4. OBJETIVO DO PROJETO",
        "5. IMPACTO DO PROBLEMA"
    )

    opportunity["B4"] = extract_section(
        text,
        "5. IMPACTO DO PROBLEMA",
        "6. URGÊNCIA E PRAZO"
    )

    opportunity["B5"] = (
        extract_after_label(
            text,
            "Urgência"
        )
    )

    opportunity["B6"] = (
        extract_first_label(
            text,
            [
                (
                    "Prazo desejado "
                    "para implantação"
                ),
                "Prazo desejado",
            ]
        )
    )

    opportunity["B7"] = (
        extract_budget(text)
    )

    opportunity["C1"] = (
        extract_decision_maker(
            text
        )
    )

    opportunity["C2"] = (
        extract_first_label(
            text,
            [
                "Influenciadores",
                "Influenciador",
            ]
        )
    )

    opportunity["C3"] = (
        extract_first_label(
            text,
            [
                (
                    "Critérios de decisão "
                    "informados"
                ),
                "Critérios de decisão",
            ]
        )
    )

    opportunity["C4"] = (
        extract_first_label(
            text,
            [
                "Concorrentes avaliados",
                "Concorrentes",
            ]
        )
    )

    # --------------------------------------------------------
    # v2.1
    # C5 agora aceita valor multilinha.
    # --------------------------------------------------------

    opportunity["C5"] = (
        extract_next_step(
            text
        )
    )

    opportunity["C6"] = (
        extract_first_label(
            text,
            [
                "Data do próximo contato",
                "Data prevista",
            ]
        )
    )

    opportunity["D1"] = (
        extract_solution(text)
    )

    opportunity["D2"] = (
        extract_scope(text)
    )

    opportunity["D3"] = (
        extract_solution_deadline(
            text
        )
    )

    opportunity["D4"] = (
        extract_solution_investment(
            text
        )
    )

    opportunity["D5"] = (
        extract_discount(text)
    )

    opportunity["D6"] = extract_section(
        text,
        "10. PREMISSAS",
        "11. EXCLUSÕES"
    )

    opportunity["D7"] = extract_section(
        text,
        "11. EXCLUSÕES",
        "12. PRÓXIMO PASSO COMERCIAL"
    )

    opportunity["E1"] = (
        extract_after_label(
            text,
            "Número da proposta"
        )
    )

    opportunity["E2"] = (
        extract_after_label(
            text,
            "Consultor responsável"
        )
    )

    opportunity["E3"] = (
        extract_after_label(
            text,
            "E-mail do consultor"
        )
    )

    opportunity["E4"] = (
        extract_issue_date(text)
    )

    opportunity["E5"] = (
        extract_after_label(
            text,
            "Idioma"
        )
    )

    opportunity["E6"] = extract_section(
        text,
        "Observações internas"
    )

    return opportunity


# ============================================================
# CATALOG
# ============================================================

def load_catalog():
    if not CATALOG_PATH.exists():
        raise FileNotFoundError(
            (
                "Catálogo JSON não encontrado: "
                f"{CATALOG_PATH}"
            )
        )

    with CATALOG_PATH.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def find_catalog_service(
    catalog,
    service_name
):
    if not is_available(
        service_name
    ):
        return None

    target = normalize(
        service_name
    )

    for service in catalog[
        "services"
    ]:
        if not service.get(
            "active",
            True
        ):
            continue

        official_name = normalize(
            service["name"]
        )

        if target == official_name:
            return service

    return None


# ============================================================
# MONEY / NUMBER PARSING
# ============================================================

def parse_brl(value):
    if not is_available(value):
        return None

    text = str(value)

    match = re.search(
        (
            r"(?:R\$\s*)?"
            r"(\d{1,3}(?:\.\d{3})*|\d+)"
            r"(?:,(\d{1,2}))?"
        ),
        text
    )

    if not match:
        return None

    integer_part = (
        match.group(1).replace(
            ".",
            ""
        )
    )

    decimal_part = (
        match.group(2)
        or "00"
    )

    if len(decimal_part) == 1:
        decimal_part += "0"

    return Decimal(
        (
            f"{integer_part}."
            f"{decimal_part}"
        )
    )


def format_brl(value):
    value = Decimal(
        value
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    formatted = (
        f"{value:,.2f}"
    )

    formatted = (
        formatted
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {formatted}"


def parse_days(value):
    if not is_available(value):
        return None

    match = re.search(
        r"(\d+)",
        str(value)
    )

    if not match:
        return None

    return int(
        match.group(1)
    )


def parse_discount_percent(
    value
):
    if not is_available(value):
        return Decimal("0")

    normalized = normalize(
        value
    )

    if (
        "nao aplicavel"
        in normalized
        or
        "sem desconto"
        in normalized
    ):
        return Decimal("0")

    match = re.search(
        r"(\d+(?:[.,]\d+)?)\s*%",
        str(value)
    )

    if not match:
        return None

    number = (
        match.group(1).replace(
            ",",
            "."
        )
    )

    return Decimal(number)


# ============================================================
# READINESS
# ============================================================

def calculate_readiness(
    opportunity
):
    dimensions = {
        "Cliente": field_available(
            "A1",
            opportunity.get("A1")
        ),

        "Problema": field_available(
            "B2",
            opportunity.get("B2")
        ),

        "Objetivo": field_available(
            "B3",
            opportunity.get("B3")
        ),

        "Impacto": field_available(
            "B4",
            opportunity.get("B4")
        ),

        "Decisor": field_available(
            "C1",
            opportunity.get("C1")
        ),

        "Orçamento": field_available(
            "B7",
            opportunity.get("B7")
        ),

        "Prazo": (
            field_available(
                "B6",
                opportunity.get("B6")
            )
            or
            field_available(
                "D3",
                opportunity.get("D3")
            )
        ),

        "Solução": field_available(
            "D1",
            opportunity.get("D1")
        ),
    }

    available = sum(
        1
        for value
        in dimensions.values()
        if value
    )

    total = len(dimensions)

    percentage = (
        available
        / total
    ) * 100

    return (
        dimensions,
        available,
        total,
        percentage
    )


def readiness_classification(
    percentage
):
    if percentage < 50:
        return "BAIXA COMPLETUDE"

    if percentage < 75:
        return "COMPLETUDE PARCIAL"

    if percentage < 100:
        return "BOA COMPLETUDE"

    return "COMPLETUDE TOTAL"


# ============================================================
# GAP ANALYSIS
# ============================================================

def find_missing_mandatory(
    opportunity
):
    missing = []

    for (
        field_id,
        description
    ) in MANDATORY_FIELDS.items():

        value = opportunity.get(
            field_id
        )

        if not field_available(
            field_id,
            value
        ):
            missing.append(
                {
                    "field": field_id,
                    "description": (
                        description
                    ),
                }
            )

    return missing


def analyze_optional_fields(
    opportunity
):
    informed = []
    missing = []

    for (
        field_id,
        description
    ) in OPTIONAL_FIELDS.items():

        value = opportunity.get(
            field_id
        )

        item = {
            "field": field_id,
            "description": description,
        }

        if field_available(
            field_id,
            value
        ):
            informed.append(item)

        else:
            missing.append(item)

    return informed, missing


# ============================================================
# PAYMENT CALCULATION
# ============================================================

def calculate_payment_terms(
    final_value,
    catalog
):
    terms = catalog[
        "commercial_policy"
    ]["payment_terms"]

    installments = []

    accumulated = Decimal(
        "0.00"
    )

    for (
        index,
        term
    ) in enumerate(terms):

        percentage = Decimal(
            str(
                term["percentage"]
            )
        )

        if index < len(terms) - 1:

            amount = (
                final_value
                * percentage
                / Decimal("100")
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            accumulated += amount

        else:
            amount = (
                final_value
                - accumulated
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

        installments.append(
            {
                "percentage": (
                    term["percentage"]
                ),
                "event": (
                    term["event"]
                ),
                "amount": amount,
            }
        )

    return installments


# ============================================================
# COMMERCIAL RULES ENGINE
# ============================================================

def validate_commercial_rules(
    opportunity,
    catalog
):
    result = {
        "service_status": (
            "BLOQUEIO"
        ),
        "service_message": "",
        "price_status": (
            "BLOQUEIO"
        ),
        "price_message": "",
        "deadline_status": (
            "BLOQUEIO"
        ),
        "deadline_message": "",
        "discount_status": "OK",
        "discount_message": "",
        "payment_status": (
            "PENDENTE"
        ),
        "payment_message": "",
        "review_status": "NÃO",
        "review_message": "",
        "service": None,
        "gross_value": None,
        "discount_percent": (
            Decimal("0")
        ),
        "discount_value": (
            Decimal("0")
        ),
        "final_value": None,
        "installments": [],
        "blocking": False,
        "requires_human_validation": (
            False
        ),
    }

    # --------------------------------------------------------
    # SERVICE
    # --------------------------------------------------------

    service_name = (
        opportunity.get("D1")
    )

    service = find_catalog_service(
        catalog,
        service_name
    )

    if service is None:

        result[
            "service_status"
        ] = "BLOQUEIO"

        result[
            "service_message"
        ] = (
            "Serviço não encontrado "
            "no catálogo."
        )

        result[
            "blocking"
        ] = True

        return result

    result["service"] = service

    result[
        "service_status"
    ] = "OK"

    result[
        "service_message"
    ] = (
        f"{service['id']} — "
        f"{service['name']}"
    )

    # --------------------------------------------------------
    # PRICE
    # --------------------------------------------------------

    proposed_value = parse_brl(
        opportunity.get("D4")
    )

    if proposed_value is None:

        result[
            "price_status"
        ] = "BLOQUEIO"

        result[
            "price_message"
        ] = (
            "Investimento não informado "
            "ou inválido."
        )

        result[
            "blocking"
        ] = True

    else:

        minimum = Decimal(
            str(
                service[
                    "investment"
                ][
                    "minimum_brl"
                ]
            )
        )

        maximum = Decimal(
            str(
                service[
                    "investment"
                ][
                    "maximum_brl"
                ]
            )
        )

        result[
            "gross_value"
        ] = proposed_value

        if proposed_value < minimum:

            result[
                "price_status"
            ] = "ALERTA"

            result[
                "price_message"
            ] = (
                f"{format_brl(proposed_value)} "
                f"abaixo da faixa "
                f"{format_brl(minimum)} a "
                f"{format_brl(maximum)}."
            )

            result[
                "requires_human_validation"
            ] = True

        elif proposed_value > maximum:

            result[
                "price_status"
            ] = "ALERTA"

            result[
                "price_message"
            ] = (
                f"{format_brl(proposed_value)} "
                f"acima da faixa "
                f"{format_brl(minimum)} a "
                f"{format_brl(maximum)}."
            )

            result[
                "requires_human_validation"
            ] = True

        else:

            result[
                "price_status"
            ] = "OK"

            result[
                "price_message"
            ] = (
                f"{format_brl(proposed_value)} "
                f"dentro da faixa "
                f"{format_brl(minimum)} a "
                f"{format_brl(maximum)}."
            )

    # --------------------------------------------------------
    # DEADLINE
    # --------------------------------------------------------

    proposed_days = parse_days(
        opportunity.get("D3")
    )

    if proposed_days is None:

        result[
            "deadline_status"
        ] = "BLOQUEIO"

        result[
            "deadline_message"
        ] = (
            "Prazo não informado "
            "ou inválido."
        )

        result[
            "blocking"
        ] = True

    else:

        minimum_days = service[
            "duration"
        ]["minimum_days"]

        maximum_days = service[
            "duration"
        ]["maximum_days"]

        if (
            proposed_days
            < minimum_days
            or
            proposed_days
            > maximum_days
        ):

            result[
                "deadline_status"
            ] = "ALERTA"

            result[
                "deadline_message"
            ] = (
                f"{proposed_days} dias "
                f"fora da faixa de "
                f"{minimum_days} a "
                f"{maximum_days} dias."
            )

            result[
                "requires_human_validation"
            ] = True

        else:

            result[
                "deadline_status"
            ] = "OK"

            result[
                "deadline_message"
            ] = (
                f"{proposed_days} dias "
                f"dentro da faixa de "
                f"{minimum_days} a "
                f"{maximum_days} dias."
            )

    # --------------------------------------------------------
    # DISCOUNT
    # --------------------------------------------------------

    discount = (
        parse_discount_percent(
            opportunity.get("D5")
        )
    )

    if discount is None:

        result[
            "discount_status"
        ] = "ALERTA"

        result[
            "discount_message"
        ] = (
            "Desconto informado "
            "em formato não reconhecido."
        )

        result[
            "requires_human_validation"
        ] = True

    elif discount == 0:

        result[
            "discount_status"
        ] = "OK"

        result[
            "discount_message"
        ] = (
            "Sem desconto aplicado."
        )

    else:

        policy = catalog[
            "commercial_policy"
        ]["discount_policy"]

        minimum_services = policy[
            "minimum_services_required"
        ]

        minimum_discount = Decimal(
            str(
                policy[
                    "minimum_discount_percent"
                ]
            )
        )

        maximum_discount = Decimal(
            str(
                policy[
                    "maximum_discount_percent"
                ]
            )
        )

        # Versão atual trabalha com
        # um serviço estruturado
        # por briefing.

        service_count = 1

        if (
            service_count
            < minimum_services
        ):

            result[
                "discount_status"
            ] = "BLOQUEIO"

            result[
                "discount_message"
            ] = (
                "Desconto não permitido "
                "para uma proposta com "
                "apenas um serviço."
            )

            result[
                "blocking"
            ] = True

        elif (
            discount
            < minimum_discount
        ):

            result[
                "discount_status"
            ] = "ALERTA"

            result[
                "discount_message"
            ] = (
                f"Desconto de "
                f"{discount}% "
                f"abaixo da faixa "
                f"autorizada."
            )

            result[
                "requires_human_validation"
            ] = True

        elif (
            discount
            > maximum_discount
        ):

            result[
                "discount_status"
            ] = "BLOQUEIO"

            result[
                "discount_message"
            ] = (
                f"Desconto de "
                f"{discount}% "
                f"acima do limite "
                f"autorizado."
            )

            result[
                "blocking"
            ] = True

        else:

            result[
                "discount_status"
            ] = "OK"

            result[
                "discount_message"
            ] = (
                f"Desconto de "
                f"{discount}% "
                f"dentro da política."
            )

    result[
        "discount_percent"
    ] = (
        discount
        if discount is not None
        else Decimal("0")
    )

    # --------------------------------------------------------
    # FINAL VALUE
    # --------------------------------------------------------

    if proposed_value is not None:

        discount_percent = result[
            "discount_percent"
        ]

        discount_value = (
            proposed_value
            * discount_percent
            / Decimal("100")
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        final_value = (
            proposed_value
            - discount_value
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        result[
            "discount_value"
        ] = discount_value

        result[
            "final_value"
        ] = final_value

        # ----------------------------------------------------
        # PAYMENT
        # ----------------------------------------------------

        installments = (
            calculate_payment_terms(
                final_value,
                catalog
            )
        )

        result[
            "installments"
        ] = installments

        installments_total = sum(
            (
                item["amount"]
                for item
                in installments
            ),
            Decimal("0.00")
        )

        if (
            installments_total
            == final_value
        ):

            result[
                "payment_status"
            ] = "OK"

            result[
                "payment_message"
            ] = (
                "Parcelas 30% / 40% / 30% "
                "fecham exatamente "
                "o valor final."
            )

        else:

            result[
                "payment_status"
            ] = "BLOQUEIO"

            result[
                "payment_message"
            ] = (
                "A soma das parcelas "
                "não corresponde "
                "ao valor final."
            )

            result[
                "blocking"
            ] = True

        # ----------------------------------------------------
        # COMMERCIAL REVIEW
        # ----------------------------------------------------

        review_policy = catalog[
            "commercial_policy"
        ]["commercial_review"]

        threshold = Decimal(
            str(
                review_policy[
                    "threshold_brl"
                ]
            )
        )

        if final_value >= threshold:

            result[
                "review_status"
            ] = "SIM"

            result[
                "review_message"
            ] = (
                "Valor final igual ou "
                "superior a "
                f"{format_brl(threshold)}."
            )

            result[
                "requires_human_validation"
            ] = True

        else:

            result[
                "review_status"
            ] = "NÃO"

            result[
                "review_message"
            ] = (
                "Valor final abaixo de "
                f"{format_brl(threshold)}."
            )

    return result


# ============================================================
# FINAL STATUS
# ============================================================

def determine_status(
    missing_mandatory,
    commercial
):
    if missing_mandatory:
        return "REQUER INFORMAÇÕES"

    if commercial["blocking"]:
        return "BLOQUEADO"

    if commercial[
        "requires_human_validation"
    ]:
        return (
            "REQUER VALIDAÇÃO HUMANA"
        )

    return (
        "APROVADO PARA "
        "RESUMO EXECUTIVO"
    )


# ============================================================
# REPORT
# ============================================================

def print_report(
    filename,
    opportunity,
    catalog
):
    (
        dimensions,
        available,
        total,
        percentage
    ) = calculate_readiness(
        opportunity
    )

    classification = (
        readiness_classification(
            percentage
        )
    )

    missing_mandatory = (
        find_missing_mandatory(
            opportunity
        )
    )

    (
        optional_informed,
        optional_missing
    ) = analyze_optional_fields(
        opportunity
    )

    commercial = (
        validate_commercial_rules(
            opportunity,
            catalog
        )
    )

    status = determine_status(
        missing_mandatory,
        commercial
    )

    total_mandatory = len(
        MANDATORY_FIELDS
    )

    complete_mandatory = (
        total_mandatory
        - len(missing_mandatory)
    )

    print()
    print("=" * 76)

    print(
        "DEALCRAFT AI — "
        "RELATÓRIO DE VALIDAÇÃO"
    )

    print("=" * 76)

    print(
        f"Arquivo: {filename}"
    )

    # --------------------------------------------------------
    # READINESS
    # --------------------------------------------------------

    print()
    print(
        "OPPORTUNITY READINESS"
    )
    print("-" * 76)

    print(
        f"{available}/{total} "
        f"dimensões disponíveis "
        f"= {percentage:.1f}%"
    )

    print(
        f"Classificação: "
        f"{classification}"
    )

    print()
    print("DIMENSÕES")
    print("-" * 76)

    for (
        dimension,
        present
    ) in dimensions.items():

        dimension_status = (
            "OK"
            if present
            else "NÃO INFORMADO"
        )

        print(
            f"{dimension:<22}"
            f"{dimension_status}"
        )

    # --------------------------------------------------------
    # MANDATORY
    # --------------------------------------------------------

    print()
    print(
        "CAMPOS OBRIGATÓRIOS"
    )
    print("-" * 76)

    print(
        f"Completos: "
        f"{complete_mandatory}/"
        f"{total_mandatory}"
    )

    print(
        f"Ausentes: "
        f"{len(missing_mandatory)}"
    )

    if missing_mandatory:

        print()
        print(
            "BLOQUEIOS IDENTIFICADOS:"
        )

        for item in (
            missing_mandatory
        ):
            print(
                f"- {item['field']} — "
                f"{item['description']}"
            )

    else:

        print()
        print(
            "Nenhum campo obrigatório "
            "ausente."
        )

    # --------------------------------------------------------
    # OPTIONAL
    # --------------------------------------------------------

    print()
    print(
        "CAMPOS OPCIONAIS"
    )
    print("-" * 76)

    print(
        f"Informados: "
        f"{len(optional_informed)}"
    )

    print(
        f"Não informados: "
        f"{len(optional_missing)}"
    )

    # --------------------------------------------------------
    # COMMERCIAL
    # --------------------------------------------------------

    print()
    print(
        "VALIDAÇÃO COMERCIAL"
    )
    print("-" * 76)

    print(
        f"Serviço: "
        f"{commercial['service_status']}"
    )

    print(
        f"  "
        f"{commercial['service_message']}"
    )

    print(
        f"Preço: "
        f"{commercial['price_status']}"
    )

    print(
        f"  "
        f"{commercial['price_message']}"
    )

    print(
        f"Prazo: "
        f"{commercial['deadline_status']}"
    )

    print(
        f"  "
        f"{commercial['deadline_message']}"
    )

    print(
        f"Desconto: "
        f"{commercial['discount_status']}"
    )

    print(
        f"  "
        f"{commercial['discount_message']}"
    )

    print(
        f"Pagamento: "
        f"{commercial['payment_status']}"
    )

    print(
        f"  "
        f"{commercial['payment_message']}"
    )

    print(
        f"Revisão comercial: "
        f"{commercial['review_status']}"
    )

    print(
        f"  "
        f"{commercial['review_message']}"
    )

    # --------------------------------------------------------
    # FINANCIAL SUMMARY
    # --------------------------------------------------------

    if (
        commercial[
            "final_value"
        ]
        is not None
    ):

        print()
        print(
            "RESUMO FINANCEIRO"
        )
        print("-" * 76)

        print(
            "Investimento bruto: "
            f"{format_brl(commercial['gross_value'])}"
        )

        print(
            "Desconto: "
            f"{commercial['discount_percent']}%"
        )

        print(
            "Valor do desconto: "
            f"{format_brl(commercial['discount_value'])}"
        )

        print(
            "Investimento final: "
            f"{format_brl(commercial['final_value'])}"
        )

        print()
        print(
            "CONDIÇÕES DE PAGAMENTO"
        )

        for installment in (
            commercial[
                "installments"
            ]
        ):
            print(
                f"- "
                f"{installment['percentage']}% "
                f"na/no "
                f"{installment['event']} — "
                f"{format_brl(installment['amount'])}"
            )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    print()
    print("RESULTADO")
    print("-" * 76)

    print(status)

    print()
    print(
        "GERAÇÃO DA PROPOSTA"
    )
    print("-" * 76)

    if status == (
        "APROVADO PARA "
        "RESUMO EXECUTIVO"
    ):

        print(
            "APTA PARA "
            "RESUMO EXECUTIVO"
        )

    elif status == (
        "REQUER VALIDAÇÃO HUMANA"
    ):

        print(
            "AGUARDANDO "
            "VALIDAÇÃO HUMANA"
        )

    else:

        print(
            "NÃO AUTORIZADA"
        )

    print("=" * 76)


# ============================================================
# DEBUG
# ============================================================

def print_opportunity_model(
    opportunity
):
    print()
    print("=" * 76)

    print(
        "OPPORTUNITY MODEL — DEBUG"
    )

    print("=" * 76)

    for field_id in sorted(
        opportunity.keys()
    ):
        value = opportunity[
            field_id
        ]

        print()
        print(
            f"{field_id}:"
        )

        if value:
            print(value)

        else:
            print(
                "NÃO INFORMADO"
            )

    print("=" * 76)


# ============================================================
# PROCESS
# ============================================================

def process_file(
    input_path,
    debug=False
):
    if not input_path.is_absolute():

        input_path = (
            BASE_DIR
            / input_path
        )

    input_path = (
        input_path.resolve()
    )

    if not input_path.exists():

        print()

        print(
            "ERRO: arquivo "
            "não encontrado: "
            f"{input_path}"
        )

        return 1

    try:

        text = (
            input_path.read_text(
                encoding="utf-8"
            )
        )

        catalog = load_catalog()

    except UnicodeDecodeError:

        print()

        print(
            "ERRO: não foi possível "
            "ler o briefing como UTF-8."
        )

        return 1

    except json.JSONDecodeError as error:

        print()

        print(
            "ERRO: catálogo JSON "
            "inválido."
        )

        print(error)

        return 1

    except FileNotFoundError as error:

        print()

        print(
            f"ERRO: {error}"
        )

        return 1

    opportunity = (
        extract_opportunity(
            text
        )
    )

    if debug:

        print_opportunity_model(
            opportunity
        )

    print_report(
        input_path.name,
        opportunity,
        catalog
    )

    return 0


# ============================================================
# CLI
# ============================================================

def print_usage():
    print()

    print(
        "DEALCRAFT AI — "
        "OPPORTUNITY VALIDATOR 2.1"
    )

    print()
    print("Uso:")

    print(
        "python dealcraft_validator.py "
        ".\\examples\\briefing-completo.txt"
    )

    print()
    print("Debug:")

    print(
        "python dealcraft_validator.py "
        ".\\examples\\briefing-completo.txt "
        "--debug"
    )


def main():
    if len(sys.argv) < 2:

        print_usage()

        return 1

    input_path = Path(
        sys.argv[1]
    )

    debug = (
        "--debug"
        in sys.argv[2:]
    )

    return process_file(
        input_path,
        debug
    )


if __name__ == "__main__":
    sys.exit(
        main()
    )