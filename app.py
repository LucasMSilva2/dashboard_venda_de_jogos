from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__, title='Dashboard Jogos')

data = pd.read_csv('vgsales.csv')

colors = {
    'background': '#121214',
    'text': '#c4c4c4'
}

#Pre-processamento
data = data.rename(columns={'Name': 'Nome', 'Platform': 'Plataforma', 'Year': 'Ano', 'Genre': 'Genero', 'Publisher': 'Editora', 'NA_Sales': 'Vendas_NA', 'EU_Sales': 'Vendas_EU', 
                            'JP_Sales': 'Vendas_JP', 'Other_Sales': 'Vendas_Outros', 'Global_Sales': 'Vendas_Globais'})
data = data[data['Ano'] <= 2016]

data.isna().sum()

data = data.dropna(subset=['Editora', 'Ano'], axis=0)
data = data.reset_index(drop=True)
data.isna().sum()

# Convertendo ano em float para int
data['Ano'] = data['Ano'].astype(int)
data['Ano'].dtype

#------------Amostra de dados do dataset------------------------

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

#------------1 - Qual genero que mais vende------------------------
GenreTotalGames = data['Vendas_Globais'].groupby(data['Genero']).sum().sort_values(ascending=False).to_frame()

fig = go.Figure(data=[go.Pie(labels=GenreTotalGames.index,
                             values=GenreTotalGames['Vendas_Globais'], opacity=0.9)])
                            
fig.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#000000', width=3.5)))
fig.update_layout(title_text='Qual gênero que mais vende',
                  title_x=0.5, title_font=dict(size=30))

fig.update_layout(
  plot_bgcolor=colors['background'],
  paper_bgcolor=colors['background'],
  font_color=colors['text']
)

#------------2 - Numero de jogos publicados por cada desenvolvedora------------------------

PublisherCount = data.groupby(pd.Grouper(key='Editora')).size().reset_index(name='count')
fig2 = px.treemap(PublisherCount, path=['Editora'], values='count')
fig2.update_layout(title_text='Numero de jogos publicados por cada desenvolvedora',
                  title_x=0.5, title_font=dict(size=22)
                  )
fig2.update_traces(textinfo="label+value")

fig2.update_layout(
  plot_bgcolor=colors['background'],
  paper_bgcolor=colors['background'],
  font_color=colors['text']
)

#------------3 - Jogos publicados por ano------------------------

AnnualNumberOfGames = data['Ano'].groupby(data['Ano']).count()

fig3 = px.bar(AnnualNumberOfGames, x=AnnualNumberOfGames.index, y=AnnualNumberOfGames,
              labels={
                  "index": "Ano",
                  "y": "Numero de Jogos Publicados"
              }
              )
fig3.update_layout(title_text='Numero de jogos publicados anualmente (Considerando suas vendas)',
                  title_x=0.5, title_font=dict(size=24))

fig3.update_layout(
  plot_bgcolor=colors['background'],
  paper_bgcolor=colors['background'],
  font_color=colors['text']
)

#------------4 - Jogo do por ano------------------------

GameGlobalSales_by_year = data.groupby('Ano').apply(lambda x: x.loc[x['Vendas_Globais'].idxmax()])

fig4 = px.bar(data_frame=GameGlobalSales_by_year, x='Ano', y='Vendas_Globais', color='Nome')

fig4.update_layout(title_text='Jogo do ano de cada ano (GOTY - The Game Awards)',
                  title_x=0.5, title_font=dict(size=20))
fig4.update_traces(marker=dict(line=dict(color='#000000', width=3)))

fig4.update_layout(
  plot_bgcolor=colors['background'],
  paper_bgcolor=colors['background'],
  font_color=colors['text']
)

#------------5 - vendas globais das desenolvedoras------------------------

top_developer_sales = data.loc[data.groupby('Editora')['Vendas_Globais'].idxmax()]
top_developer_sales = top_developer_sales.sort_values(by='Vendas_Globais', ascending=False).nlargest(15, 'Vendas_Globais')

fig5 = px.bar(top_developer_sales, x='Editora', y='Vendas_Globais', color='Nome',
             labels={
                 "Editora": "Editora",
                 "Vendas_Globais": "Vendas Globais"
             },
             title="Ranking das desenvolvedoras e seus jogos mais vendidos",
             template='ggplot2')

fig5.update_layout(xaxis={'categoryorder': 'total descending'})

fig5.update_layout(
  plot_bgcolor=colors['background'],
  paper_bgcolor=colors['background'],
  font_color=colors['text']
)

#------------6 -Plus - Top 10 plataformas mais vendidas globalmente------------------------

PlatformGlobalSales = data['Vendas_Globais'].groupby(data['Plataforma']).sum().sort_values(ascending=False).to_frame()
PlatformGlobalSales = PlatformGlobalSales.nlargest(10, 'Vendas_Globais')[['Vendas_Globais']]

fig6 = px.bar(data_frame=PlatformGlobalSales, x=PlatformGlobalSales.index, y='Vendas_Globais', color=PlatformGlobalSales.index)
fig6.update_layout(title_text='Maiores vendas de plataforma em escala global',
                  title_x=0.5, title_font=dict(size=20))
fig6.update_layout(xaxis={'categoryorder': 'total descending'})
fig6.update_traces(marker=dict(line=dict(color='#000000', width=2)))

fig6.update_layout(
  plot_bgcolor=colors['background'],
  paper_bgcolor=colors['background'],
  font_color=colors['text']
)

#------7 Comparação de vendas globais por plataforma PC X Console------------------------
PS = data[data['Plataforma'] == 'PS'].groupby('Ano')['Vendas_Globais'].sum().reset_index()
PS2 = data[data['Plataforma'] == 'PS2'].groupby('Ano')['Vendas_Globais'].sum().reset_index()
PS3 = data[data['Plataforma'] == 'PS3'].groupby('Ano')['Vendas_Globais'].sum().reset_index()
PS4 = data[data['Plataforma'] == 'PS4'].groupby('Ano')['Vendas_Globais'].sum().reset_index()
PC = data[data['Plataforma'] == 'PC'].groupby('Ano')['Vendas_Globais'].sum().reset_index()

fig7 = go.Figure()
fig7.add_trace(go.Scatter(x=PS['Ano'], y=PS['Vendas_Globais'],
                         name="Vendas PS",
                         hovertext=PS['Vendas_Globais']))

fig7.add_trace(go.Scatter(x=PS2['Ano'], y=PS2['Vendas_Globais'],
                         name="Vendas PS2",
                         hovertext=PS2['Vendas_Globais']))

fig7.add_trace(go.Scatter(x=PS3['Ano'], y=PS3['Vendas_Globais'],
                         name="Vendas PS3",
                         hovertext=PS3['Vendas_Globais']))

fig7.add_trace(go.Scatter(x=PS4['Ano'], y=PS4['Vendas_Globais'],
                         name="Vendas PS4",
                         hovertext=PS4['Vendas_Globais']))

fig7.add_trace(go.Scatter(x=PC['Ano'], y=PC['Vendas_Globais'],
                         name="Vendas PC",
                         hovertext=PC['Vendas_Globais']))

fig7.update_layout(title_text='Playstations vs PC | Comparação de Vendas Globais (1985 a 2017)',
                  title_x=0.5, title_font=dict(size=22))  
fig7.update_layout(
    xaxis_title="Ano",
    yaxis_title="Vendas Globais (M)")

fig7.update_layout(
  plot_bgcolor=colors['background'],
  paper_bgcolor=colors['background'],
  font_color=colors['text'] 
)

#Plus - Top 10 plataformas mais vendidas globalmente


app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.H1('Dashboard Jogos', className="app-header--title")
        ]
    ),

    html.Div(
        className="content",
        children=[
            html.Div(
                className="overview",
                children=[
                    html.H1('Overview'),
                    html.P('''Este dashboard contempla a análise de um dataset robusto sobre vendas de jogos.
                        Com base nisso, exploraremos os dados afim de obtermos gráficos que auxiliem na tomada de decisões.''')
                ]
            ),
        ]   
    ),

  html.H1(
    className="equipe",
    children=("Equipe de Desenvolvimento")
  ),

  html.Div(
    className="whapper",
    children=[
      #Lucas Torres
      html.Aside(
        className="sidebar",
        children=[
          html.Img(
            className="cover",
            src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=40",
          ),
          html.Div(
            className="profile",
            children=[
              html.Img(
                className="avatar",
                src="https://github.com/LucasMSilva2.png",
              ),

              html.Strong("Lucas Torres"),
              html.Span("Web Developer")
            ]
          ),

          html.Footer(
            children=(
              html.A(
                href='https://www.linkedin.com/in/lucas-torres-4781b0214/',
                target="blank",
                children=[
                  "linkedin"
                ]
              ),
            )
          )  
        ]
      ),
      #Marcos Antônio
      html.Aside(
        className="sidebar",
        children=[
          html.Img(
            className="cover",
            src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=40",
          ),
          html.Div(
            className="profile",
            children=[
              html.Img(
                className="avatar",
                src="https://github.com/MarcosDex.png",
              ),

              html.Strong("Marcos Antônio"),
              html.Span("Web Developer")
            ]
          ),

          html.Footer(
            children=(
              html.A(
                href='https://www.linkedin.com/in/marcosdex/',
                target="blank",
                children=[
                  "linkedin"
                ]
              ),
            )
          )  
        ]
      ),

      html.Aside(
        className="sidebar",
        children=[
          html.Img(
            className="cover",
            src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=40",
          ),
          html.Div(
            className="profile",
            children=[
              html.Img(
                className="avatar",
                src="https://github.com/VitorVini.png",
              ),

              html.Strong("Vitor Vinícius"),
              html.Span("Web Developer")
            ]
          ),

          html.Footer(
            children=(
              html.A(
                href='https://www.linkedin.com/in/VitorViniciusSilva',
                target="blank",
                children=[
                  "linkedin"
                ]
              ),
            )
          )  
        ]
      ),
    ]
  ),

  html.Main(
    children=[
      html.Article(
        className="post",
        children=[
          html.Div(
            className="content",
            children=[
              html.H2(
                children='Uma pequena amostra dos dados que iremos trabalhar',
                style={"margin": "auto"}
              ),
              generate_table(data)
            ]
          ),

          html.Div(
            className="comment",
            children=[
              html.Strong("Comentário"),

              html.Div(
                className="textarea",
                children=[
                  html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci maxime magnam repudiandae quis recusandae ad pariatur. Cumque odio distinctio porro iste dolores a totam minus tempora. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci")
                ]
              )
            ]
          ),
        ]
      ),

      html.Article(
        className="post",
        children=[
          html.Div(
            className="content",
            children=[
              dcc.Graph(
                id='genero',
                figure=fig,
              ),
            ]
          ),

          html.Div(
            className="comment",
            children=[
              html.Strong("Comentário"),

              html.Div(
                className="textarea",
                children=[
                  html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci maxime magnam repudiandae quis recusandae ad pariatur. Cumque odio distinctio porro iste dolores a totam minus tempora. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci")
                ]
              )
            ]
          ),
        ]
      ),

      html.Article(
        className="post",
        children=[
          html.Div(
            className="content",
            children=[
              dcc.Graph(
                id='jogosPublicadosDesen',
                figure=fig2,
              ),
            ]
          ),

          html.Div(
            className="comment",
            children=[
              html.Strong("Comentário"),

              html.Div(
                className="textarea",
                children=[
                  html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci maxime magnam repudiandae quis recusandae ad pariatur. Cumque odio distinctio porro iste dolores a totam minus tempora. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci")
                ]
              )
            ]
          ),
        ]
      ),

      html.Article(
        className="post",
        children=[
          html.Div(
            className="content",
            children=[
              dcc.Graph(
                id='jogosPublicadosAno',
                figure=fig3,
              ),
            ]
          ),

          html.Div(
            className="comment",
            children=[
              html.Strong("Comentário"),

              html.Div(
                className="textarea",
                children=[
                  html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci maxime magnam repudiandae quis recusandae ad pariatur. Cumque odio distinctio porro iste dolores a totam minus tempora. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci")
                ]
              )
            ]
          ),
        ]
      ),

      html.Article(
        className="post",
        children=[
          html.Div(
            className="content",
            children=[
              dcc.Graph(
                id='jogosDoAno',
                figure=fig4,
              ),
            ]
          ),

          html.Div(
            className="comment",
            children=[
              html.Strong("Comentário"),

              html.Div(
                className="textarea",
                children=[
                  html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci maxime magnam repudiandae quis recusandae ad pariatur. Cumque odio distinctio porro iste dolores a totam minus tempora. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci")
                ]
              )
            ]
          ),
        ]
      ),

      html.Article(
        className="post",
        children=[
          html.Div(
            className="content",
            children=[
              dcc.Graph(
                id='vendasGlobaisDesen',
                figure=fig5,
              ),
            ]
          ),

          html.Div(
            className="comment",
            children=[
              html.Strong("Comentário"),

              html.Div(
                className="textarea",
                children=[
                  html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci maxime magnam repudiandae quis recusandae ad pariatur. Cumque odio distinctio porro iste dolores a totam minus tempora. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci")
                ]
              )
            ]
          ),
        ]
      ),

      html.Article(
        className="post",
        children=[
          html.Div(
            className="content",
            children=[
              dcc.Graph(
                id='Top10Plataformas',
                figure=fig6,
              ),
            ]
          ),

          html.Div(
            className="comment",
            children=[
              html.Strong("Comentário"),

              html.Div(
                className="textarea",
                children=[
                  html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci maxime magnam repudiandae quis recusandae ad pariatur. Cumque odio distinctio porro iste dolores a totam minus tempora. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci")
                ]
              )
            ]
          ),
        ]
      ),

      html.Article(
        className="post",
        children=[
          html.Div(
            className="content",
            children=[
              dcc.Graph(
                id='vendasPCXConsole',
                figure=fig7,
              ),
            ]
          ),

          html.Div(
            className="comment",
            children=[
              html.Strong("Comentário"),

              html.Div(
                className="textarea",
                children=[
                  html.P("Lorem ipsum dolor sit amet consectetur adipisicing elit. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci maxime magnam repudiandae quis recusandae ad pariatur. Cumque odio distinctio porro iste dolores a totam minus tempora. Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim impedit reiciendis harum adipisci")
                ]
              )
            ]
          ),
        ]
      ),
    ]
  )


    
])

if __name__ == '__main__':
    app.run_server(debug=True)