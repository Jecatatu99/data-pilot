import streamlit as st

from src.agent import answer_question_locally
from src.charts import (
    create_monthly_revenue_chart,
    create_top_cities_chart,
)
from src.metrics import (
    calculate_average_revenue_per_customer,
    calculate_average_ticket,
    calculate_cancellation_rate,
    calculate_completed_orders,
    calculate_total_revenue,
    calculate_unique_customers,
    load_clean_data,
)


st.set_page_config(
    page_title="Data Pilot",
    page_icon="📊",
    layout="wide",
)


def format_brl(value: float) -> str:
    """Formata um valor monetário no padrão brasileiro."""

    formatted = (
        f"{value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {formatted}"


def format_percentage(value: float) -> str:
    """Formata um percentual no padrão brasileiro."""

    return f"{value:.2f}%".replace(".", ",")


@st.cache_data
def load_application_data():
    """Carrega e valida a base tratada."""

    df = load_clean_data()

    required_columns = {
        "order_id",
        "order_date",
        "customer_id",
        "category",
        "city",
        "quantity",
        "unit_price",
        "status",
        "revenue",
    }

    missing_columns = required_columns.difference(
        df.columns
    )

    if missing_columns:
        columns_text = ", ".join(
            sorted(missing_columns)
        )

        raise ValueError(
            "A base tratada não possui as colunas obrigatórias: "
            f"{columns_text}"
        )

    if df.empty:
        raise ValueError(
            "A base tratada está vazia."
        )

    return df


def apply_category_filter(
    df,
    selected_category: str,
):
    """Aplica o filtro de categoria."""

    if selected_category == "Todas":
        return df.copy()

    return df.loc[
        df["category"] == selected_category
    ].copy()


def initialize_chat_history() -> None:
    """Cria o histórico inicial da conversa."""

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "Olá! Pergunte sobre receita total, pedidos "
                    "concluídos, ticket médio, clientes únicos, "
                    "taxa de cancelamento ou receita média por cliente."
                ),
                "tool": None,
            }
        ]


def show_metric_cards(filtered_df) -> None:
    """Calcula e exibe os cards do painel."""

    total_revenue = calculate_total_revenue(
        filtered_df
    )

    completed_orders = calculate_completed_orders(
        filtered_df
    )

    average_ticket = calculate_average_ticket(
        filtered_df
    )

    unique_customers = calculate_unique_customers(
        filtered_df
    )

    cancellation_rate = calculate_cancellation_rate(
        filtered_df
    )

    revenue_per_customer = (
        calculate_average_revenue_per_customer(
            filtered_df
        )
    )

    first_row = st.columns(3)

    first_row[0].metric(
        label="Receita total",
        value=format_brl(total_revenue),
    )

    first_row[1].metric(
        label="Pedidos concluídos",
        value=completed_orders,
    )

    first_row[2].metric(
        label="Ticket médio",
        value=format_brl(average_ticket),
    )

    second_row = st.columns(3)

    second_row[0].metric(
        label="Clientes únicos",
        value=unique_customers,
    )

    second_row[1].metric(
        label="Taxa de cancelamento",
        value=format_percentage(
            cancellation_rate
        ),
    )

    second_row[2].metric(
        label="Receita média por cliente",
        value=format_brl(
            revenue_per_customer
        ),
    )


def show_charts(filtered_df) -> None:
    """Exibe os gráficos do painel."""

    st.divider()
    st.subheader("Análise visual")

    monthly_chart = create_monthly_revenue_chart(
        filtered_df
    )

    cities_chart = create_top_cities_chart(
        filtered_df,
        limit=5,
    )

    monthly_column, cities_column = st.columns(2)

    with monthly_column:
        st.plotly_chart(
            monthly_chart,
            use_container_width=True,
        )

    with cities_column:
        st.plotly_chart(
            cities_chart,
            use_container_width=True,
        )


def show_sales_dashboard(
    df,
    selected_category: str,
) -> None:
    """Exibe o painel de vendas."""

    filtered_df = apply_category_filter(
        df,
        selected_category,
    )

    st.title("📊 Data Pilot")

    st.write(
        "Painel inteligente para análise "
        "de dados fictícios de vendas."
    )

    if selected_category == "Todas":
        st.caption(
            "Os indicadores consideram todas as categorias."
        )
    else:
        st.caption(
            f"Os indicadores consideram somente a categoria "
            f"**{selected_category}**."
        )

    st.subheader("Indicadores principais")

    show_metric_cards(filtered_df)
    show_charts(filtered_df)

    st.divider()

    st.subheader("Dados utilizados")

    st.write(
        f"Registros disponíveis no filtro: "
        f"**{len(filtered_df)}**"
    )

    with st.expander(
        "Visualizar amostra dos dados",
        expanded=False,
    ):
        st.dataframe(
            filtered_df.head(20),
            use_container_width=True,
            hide_index=True,
        )


def show_chat(
    df,
    selected_category: str,
) -> None:
    """Exibe a conversa com os dados."""

    filtered_df = apply_category_filter(
        df,
        selected_category,
    )

    initialize_chat_history()

    st.title("💬 Converse com os dados")

    st.write(
        "Faça uma pergunta em português. "
        "O Python selecionará uma ferramenta e calculará a resposta."
    )

    if selected_category == "Todas":
        st.info(
            "As respostas consideram todas as categorias."
        )
    else:
        st.info(
            f"As respostas consideram somente a categoria "
            f"**{selected_category}**."
        )

    with st.expander(
        "Exemplos de perguntas",
        expanded=False,
    ):
        st.markdown(
            """
- Qual foi a receita total?
- Quantos pedidos foram concluídos?
- Qual é o ticket médio?
- Quantos clientes diferentes compraram?
- Qual foi a taxa de cancelamento?
- Qual foi a receita média por cliente?
            """
        )

    for message in st.session_state.chat_messages:
        with st.chat_message(
            message["role"]
        ):
            st.markdown(
                message["content"]
            )

            if message.get("tool"):
                st.caption(
                    "Ferramenta utilizada: "
                    f"`{message['tool']}`"
                )

    question = st.chat_input(
        "Digite sua pergunta sobre os dados"
    )

    if question:
        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": question,
                "tool": None,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner(
                    "Analisando a pergunta e "
                    "calculando a métrica..."
                ):
                    response = answer_question_locally(
                        question,
                        filtered_df,
                    )

                st.markdown(
                    response["answer"]
                )

                if response["tool_name"]:
                    st.caption(
                        "Ferramenta utilizada: "
                        f"`{response['tool_name']}`"
                    )

                assistant_message = {
                    "role": "assistant",
                    "content": response["answer"],
                    "tool": response["tool_name"],
                }

            except ValueError as error:
                error_message = (
                    "Não foi possível executar a ferramenta "
                    f"solicitada: {error}"
                )

                st.warning(error_message)

                assistant_message = {
                    "role": "assistant",
                    "content": error_message,
                    "tool": None,
                }

            except Exception:
                error_message = (
                    "Não foi possível responder à pergunta. "
                    "Tente novamente usando um dos exemplos disponíveis."
                )

                st.error(error_message)

                assistant_message = {
                    "role": "assistant",
                    "content": error_message,
                    "tool": None,
                }

        st.session_state.chat_messages.append(
            assistant_message
        )

    clear_column, information_column = st.columns(
        [1, 4]
    )

    with clear_column:
        if st.button(
            "Limpar conversa",
            use_container_width=True,
        ):
            st.session_state.chat_messages = []
            st.rerun()

    with information_column:
        st.caption(
            "Modo local ativo. O provedor externo de IA está "
            "indisponível na rede corporativa. Os valores são "
            "sempre calculados pelas funções Python."
        )


def main() -> None:
    """Controla os menus e filtros da aplicação."""

    try:
        df = load_application_data()

    except FileNotFoundError:
        st.error(
            "O arquivo tratado de vendas não foi encontrado."
        )

        st.info(
            "Execute o comando abaixo e reinicie o aplicativo:"
        )

        st.code(
            "python src/data_processing.py",
            language="bash",
        )

        st.stop()

    except ValueError as error:
        st.error(
            "A base de vendas não pôde ser validada."
        )

        st.warning(
            str(error)
        )

        st.stop()

    except Exception:
        st.error(
            "Ocorreu um erro inesperado ao carregar os dados."
        )

        st.info(
            "Confira se o arquivo sales_clean.csv existe "
            "e se todas as dependências foram instaladas."
        )

        st.stop()

    st.sidebar.title("Data Pilot")

    st.sidebar.caption(
        "Painel e conversa com os dados"
    )

    selected_page = st.sidebar.radio(
        label="Navegação",
        options=[
            "Painel de vendas",
            "Converse com os dados",
        ],
    )

    categories = sorted(
        df["category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_category = st.sidebar.selectbox(
        label="Filtrar por categoria",
        options=[
            "Todas",
            *categories,
        ],
    )

    st.sidebar.divider()

    filtered_count = len(
        apply_category_filter(
            df,
            selected_category,
        )
    )

    st.sidebar.metric(
        label="Registros no filtro",
        value=filtered_count,
    )

    st.sidebar.caption(
        "Base fictícia criada para fins educacionais."
    )

    if selected_page == "Painel de vendas":
        show_sales_dashboard(
            df,
            selected_category,
        )
    else:
        show_chat(
            df,
            selected_category,
        )


if __name__ == "__main__":
    main()