from pathlib import Path
import sys

from dealcraft_validator import (
    extract_opportunity,
    load_catalog,
    calculate_readiness,
    readiness_classification,
    find_missing_mandatory,
    validate_commercial_rules,
    determine_status,
    format_brl,
    is_available,
)


# ============================================================
# DEALCRAFT AI — EXECUTIVE SUMMARY ENGINE
# Version: 1.0
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# TEXT UTILITIES
# ============================================================

def safe_value(value, default="NÃO INFORMADO"):
    """
    Retorna o valor original quando disponível.
    Nunca inventa informação ausente.
    """

    if not is_available(value):
        return default

    return str(value).strip()


def compact_text(value, default="NÃO INFORMADO"):
    """
    Compacta textos multilinha para apresentação no resumo.
    """

    if not is_available(value):
        return default

    lines = []

    for line in str(value).splitlines():
        clean = line.strip()

        if not clean:
            continue

        clean = clean.lstrip("-–—• ").strip()

        if clean:
            lines.append(clean)

    if not lines:
        return default

    return " ".join(lines)


# ============================================================
# EXECUTIVE SUMMARY MODEL
# ============================================================

def build_executive_summary(
    opportunity,
    commercial
):
    """
    Constrói o resumo executivo exclusivamente
    com dados existentes no Opportunity Model
    e no Commercial Rules Engine.
    """

    summary = {
        "client": safe_value(
            opportunity.get("A1")
        ),

        "sector": safe_value(
            opportunity.get("A2")
        ),

        "contact": safe_value(
            opportunity.get("A5")
        ),

        "contact_role": safe_value(
            opportunity.get("A6")
        ),

        "current_scenario": compact_text(
            opportunity.get("B1")
        ),

        "problem": compact_text(
            opportunity.get("B2")
        ),

        "objective": compact_text(
            opportunity.get("B3")
        ),

        "impact": compact_text(
            opportunity.get("B4")
        ),

        "urgency": safe_value(
            opportunity.get("B5")
        ),

        "desired_deadline": safe_value(
            opportunity.get("B6")
        ),

        "budget": safe_value(
            opportunity.get("B7")
        ),

        "decision_maker": safe_value(
            opportunity.get("C1")
        ),

        "decision_criteria": safe_value(
            opportunity.get("C3")
        ),

        "next_step": safe_value(
            opportunity.get("C5")
        ),

        "next_contact": safe_value(
            opportunity.get("C6")
        ),

        "service": safe_value(
            opportunity.get("D1")
        ),

        "scope": compact_text(
            opportunity.get("D2")
        ),

        "deadline": safe_value(
            opportunity.get("D3")
        ),

        "proposal_number": safe_value(
            opportunity.get("E1")
        ),

        "consultant": safe_value(
            opportunity.get("E2")
        ),

        "issue_date": safe_value(
            opportunity.get("E4")
        ),
    }

    if commercial["gross_value"] is not None:
        summary["gross_value"] = format_brl(
            commercial["gross_value"]
        )
    else:
        summary["gross_value"] = "NÃO INFORMADO"

    summary["discount"] = (
        f"{commercial['discount_percent']}%"
    )

    if commercial["final_value"] is not None:
        summary["final_value"] = format_brl(
            commercial["final_value"]
        )
    else:
        summary["final_value"] = "NÃO INFORMADO"

    summary["commercial_review"] = (
        commercial["review_status"]
    )

    summary["installments"] = []

    for installment in commercial["installments"]:
        summary["installments"].append(
            {
                "percentage": installment[
                    "percentage"
                ],
                "event": installment["event"],
                "amount": format_brl(
                    installment["amount"]
                ),
            }
        )

    return summary


# ============================================================
# SUMMARY OUTPUT
# ============================================================

def print_executive_summary(
    summary,
    readiness_percentage,
    readiness_label
):
    print()
    print("=" * 78)
    print("DEALCRAFT AI — RESUMO EXECUTIVO DA OPORTUNIDADE")
    print("=" * 78)

    print()
    print("1. CLIENTE")
    print("-" * 78)

    print(
        f"Empresa: {summary['client']}"
    )

    print(
        f"Setor: {summary['sector']}"
    )

    print(
        f"Contato principal: "
        f"{summary['contact']}"
    )

    print(
        f"Cargo: {summary['contact_role']}"
    )

    print()
    print("2. OPORTUNIDADE")
    print("-" * 78)

    print(
        f"Cenário atual: "
        f"{summary['current_scenario']}"
    )

    print(
        f"Problema principal: "
        f"{summary['problem']}"
    )

    print(
        f"Objetivo: "
        f"{summary['objective']}"
    )

    print(
        f"Impacto: "
        f"{summary['impact']}"
    )

    print(
        f"Urgência: "
        f"{summary['urgency']}"
    )

    print(
        f"Prazo desejado: "
        f"{summary['desired_deadline']}"
    )

    print(
        f"Orçamento informado: "
        f"{summary['budget']}"
    )

    print()
    print("3. PROCESSO DECISÓRIO")
    print("-" * 78)

    print(
        f"Decisor: "
        f"{summary['decision_maker']}"
    )

    print(
        f"Critérios de decisão: "
        f"{summary['decision_criteria']}"
    )

    print(
        f"Próximo passo: "
        f"{summary['next_step']}"
    )

    print(
        f"Próximo contato: "
        f"{summary['next_contact']}"
    )

    print()
    print("4. SOLUÇÃO PROPOSTA")
    print("-" * 78)

    print(
        f"Serviço: "
        f"{summary['service']}"
    )

    print(
        f"Escopo: "
        f"{summary['scope']}"
    )

    print(
        f"Prazo: "
        f"{summary['deadline']}"
    )

    print()
    print("5. CONDIÇÕES COMERCIAIS")
    print("-" * 78)

    print(
        f"Investimento bruto: "
        f"{summary['gross_value']}"
    )

    print(
        f"Desconto: "
        f"{summary['discount']}"
    )

    print(
        f"Investimento final: "
        f"{summary['final_value']}"
    )

    if summary["installments"]:
        print()
        print("Pagamento:")

        for installment in summary[
            "installments"
        ]:
            print(
                f"- {installment['percentage']}% "
                f"na/no {installment['event']} — "
                f"{installment['amount']}"
            )

    print()
    print(
        f"Revisão comercial obrigatória: "
        f"{summary['commercial_review']}"
    )

    print()
    print("6. CONTROLE")
    print("-" * 78)

    print(
        f"Proposta: "
        f"{summary['proposal_number']}"
    )

    print(
        f"Consultor: "
        f"{summary['consultant']}"
    )

    print(
        f"Data de emissão: "
        f"{summary['issue_date']}"
    )

    print()
    print("7. OPPORTUNITY READINESS")
    print("-" * 78)

    print(
        f"{readiness_percentage:.1f}% — "
        f"{readiness_label}"
    )

    print()
    print("=" * 78)


# ============================================================
# HUMAN-IN-THE-LOOP
# ============================================================

def request_human_approval():
    """
    Solicita confirmação explícita antes de qualquer
    geração futura da proposta.
    """

    print()
    print("CHECKPOINT DE APROVAÇÃO HUMANA")
    print("-" * 78)

    print(
        "Revise o resumo executivo acima."
    )

    print()
    print(
        "Nenhuma proposta será gerada sem "
        "confirmação explícita."
    )

    print()
    print(
        "Digite APROVAR para autorizar a próxima etapa."
    )

    print(
        "Digite REVISAR para interromper e revisar os dados."
    )

    print()

    response = input(
        "Decisão: "
    ).strip().upper()

    if response == "APROVAR":
        return True

    return False


# ============================================================
# PROCESS
# ============================================================

def process_summary(
    input_path,
    interactive=True
):
    if not input_path.is_absolute():
        input_path = (
            BASE_DIR / input_path
        )

    input_path = input_path.resolve()

    if not input_path.exists():
        print()
        print(
            f"ERRO: arquivo não encontrado: "
            f"{input_path}"
        )
        return 1

    try:
        text = input_path.read_text(
            encoding="utf-8"
        )

        catalog = load_catalog()

    except UnicodeDecodeError:
        print()
        print(
            "ERRO: não foi possível ler "
            "o briefing como UTF-8."
        )
        return 1

    except Exception as error:
        print()
        print(
            f"ERRO: {error}"
        )
        return 1

    opportunity = extract_opportunity(
        text
    )

    (
        dimensions,
        available,
        total,
        percentage
    ) = calculate_readiness(
        opportunity
    )

    readiness_label = (
        readiness_classification(
            percentage
        )
    )

    missing_mandatory = (
        find_missing_mandatory(
            opportunity
        )
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

    # --------------------------------------------------------
    # GATE
    # --------------------------------------------------------

    if status != (
        "APROVADO PARA RESUMO EXECUTIVO"
    ):
        print()
        print("=" * 78)
        print(
            "DEALCRAFT AI — RESUMO EXECUTIVO"
        )
        print("=" * 78)

        print()
        print(
            f"Status da oportunidade: {status}"
        )

        print()
        print(
            "O resumo executivo não pode ser "
            "liberado nesta etapa."
        )

        if missing_mandatory:
            print()
            print(
                "Campos obrigatórios pendentes:"
            )

            for item in missing_mandatory:
                print(
                    f"- {item['field']} — "
                    f"{item['description']}"
                )

        if commercial["blocking"]:
            print()
            print(
                "Existem bloqueios nas regras "
                "comerciais."
            )

        if commercial[
            "requires_human_validation"
        ]:
            print()
            print(
                "A oportunidade requer "
                "validação humana."
            )

        print()
        print(
            "GERAÇÃO DA PROPOSTA: "
            "NÃO AUTORIZADA"
        )

        print("=" * 78)

        return 2

    # --------------------------------------------------------
    # BUILD SUMMARY
    # --------------------------------------------------------

    summary = build_executive_summary(
        opportunity,
        commercial
    )

    print_executive_summary(
        summary,
        percentage,
        readiness_label
    )

    # --------------------------------------------------------
    # HUMAN APPROVAL
    # --------------------------------------------------------

    if not interactive:
        return 0

    approved = request_human_approval()

    if approved:
        print()
        print("=" * 78)
        print(
            "APROVAÇÃO HUMANA REGISTRADA"
        )
        print("=" * 78)

        print()
        print(
            "Status: APROVADO PARA GERAÇÃO DA PROPOSTA"
        )

        print()
        print(
            "O DealCraft AI está autorizado "
            "a avançar para a etapa de geração "
            "do documento."
        )

        print()
        print(
            "Observação: nesta versão, o arquivo "
            ".docx ainda não será gerado."
        )

        print(
            "A geração será implementada na "
            "próxima fase."
        )

        print("=" * 78)

        return 0

    print()
    print("=" * 78)
    print(
        "APROVAÇÃO NÃO CONCEDIDA"
    )
    print("=" * 78)

    print()
    print(
        "Status: REVISÃO NECESSÁRIA"
    )

    print()
    print(
        "Nenhuma proposta foi gerada."
    )

    print("=" * 78)

    return 3


# ============================================================
# CLI
# ============================================================

def print_usage():
    print()
    print(
        "DEALCRAFT AI — EXECUTIVE SUMMARY ENGINE 1.0"
    )

    print()
    print("Uso:")

    print(
        "python dealcraft_summary.py "
        ".\\examples\\briefing-completo.txt"
    )

    print()
    print("Validação sem interação:")

    print(
        "python dealcraft_summary.py "
        ".\\examples\\briefing-completo.txt "
        "--no-input"
    )


def main():
    if len(sys.argv) < 2:
        print_usage()
        return 1

    input_path = Path(
        sys.argv[1]
    )

    interactive = (
        "--no-input"
        not in sys.argv[2:]
    )

    return process_summary(
        input_path,
        interactive
    )


if __name__ == "__main__":
    sys.exit(
        main()
    )