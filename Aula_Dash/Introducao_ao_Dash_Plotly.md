# 🚀 Introdução à Biblioteca Dash da Plotly

## **Introdução**

O objetivo deste material é introduzir e servir como guia rápido para a utilização da biblioteca Dash em Python. Dessa forma, esse material teve como base para a sua construção a documentação disponivel na internet.

### **Algumas vantagens da biblioteca Dash**
Dash é uma ferramenta indispensável para a visualização de dados por meio da construção de uma aplicação na internet com a biblioteca plotly.py.
  * É escrita em cima de plotly.js, Flask e React.js (Foi desenvolvida por Plotly)
  * Dash é simples o bastante para construir aplicações de forma rápida
    * Possibilita a manipulação de dados e apresentação desses de forma simultânea
  * Renderizado no seu navegador da web (independente de qual seja o navegador)
  * Biblioteca código aberto 
  * Sem HTML ou JavaScript, o Dash possibilita criar interfaces em Python com inúmeros componentes interativos


### **Instalação**

Com o terminal ou prompt de comando aberto, execute o seguinte comando para atualizar o pip para a versão mais recente:

```bash
python -m pip install --upgrade pip
python.exe -m pip install --upgrade pip
```

### **Ambiente Virtual**

* Virtualenv:
```bash
pip install virtualenv
virtualenv env_proj_name
```

* venv:
```bash
python -m venv env_proj_name
python -m venv .venv
```

### **Ativar o ambiente virtual no Windows**

* cmd:
```bash
meu_ambiente\Scripts\activate.bat
.venv\Scripts\activate.bat
cd .venv/Script
activate.bat
```

* pwsh:
```bash
meu_ambiente\Scripts\Activate.ps1
.venv\Scripts\Activate.ps1
cd .venv/Script
Activate.ps1
```

### **Desativar ambiente virtual**

```bash
deactivate
```

### **Apagar um ambiente virtual**

```bash
rmdir /s /q venv
```

### **Instalar pacotes**

```bash
pip install -r requirements.txt
python -m pip install 'pacote'
```

### **Instalando o pacote Dash**

```python
pip install dash
```

**Obs.:** Para verificar se os outros pacotes foram instalados automaticamente, no seu terminal, reproduza
`pip list` ou `pip freeze` e busque pelos seus nomes.

O ``pip install dash`` instalará automaticamente os seguintes pacotes com as versões mais recentes:

- `dash-renderer`
- `dash-core-components`
- `dash-html-components`
- `dash-table`
- `plotly`

Para verificar a versão instalada do Dash:

```bash
pip show dash
```

Versão mais recente verificada: **Dash 3.0.2** (abril de 2025)

### **Verificando a versão**

```python
import dash
print(dash.__version__)
```

**Aconselho você a verificar a versão dos pacotes instalados para que você sempre esteja trabalhando com a versão mais atualizada da Biblioteca Dash e as demais instaladas automaticamente.**

## **Layout**

O layout é um componente fundamental das aplicações com a biblioteca Dash em Python. Ele é quem descreve como a aplicação se apresentará, ou seja, compreende a construção visual da aplicação web desde a parte estética até a organização dos componentes.

Para construir a parte visual da aplicação, é disponível um conjunto de componentes com as bibliotecas `dash_core_components` (dcc) e `dash_html_components` (html).

Encontre mais exemplos em [Layout](https://dash.plotly.com/layout).

### **Primeiro Exemplo - `Exemplo_1.py`**
O código desenvolvido e comentado está na pasta [Exercicios](\Exercicios)

#### **Importando os módulos necessários**

```python
import dash
from dash import dcc, html
```

#### **Ajustando o tipo de fonte usando CSS para modificar o padrão dos elementos utilizados e criando o aplicativo com a função `Dash()` da biblioteca Dash.**

```python
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
```

#### **O layout é composto por 4 elementos, ou seja, elementos do tipo `html.Div`, `html.H1` e `dcc.Graph`**.

```python
app.layout = html.Div(
    children=[

        html.H1(
            children='Apresentação da biblioteca Dash!'),

        html.Div(
            children='''
                Dash: Aplicação na internet para Python.
            '''
        ),

        dcc.Graph(
            id='example-graph',
            figure={
                'data':[
                    {'x':[0,1,2,3,4,5,6],'y':[0,1,2,3,4,5,6],'type':'line+markers','name':'Reta'},
                    {'x':[0,1,2,3,4,5,6],'y':[0,1,4,9,16,25,36],'type':'line+markers','name':'Parábola'}
                ],
                'layout':{
                    'title':'Gráfico Exemplo'
                }
            }
        ) 
    ]
)
```

No Dash já é incluso o `hot-reloading`, ou seja, graças ao
> `app.run(debug=True)`

a aplicação será autualizada automáticamente assim que alguma modificação seja feita.
Caso não queira que a página no navegador seja atualizada sempre que for feita uma modificação no código fonte, utilize
> `app.run(dev_tools_hot_reload = False)`

Entenda mais sobre no tópico [Dash Dev Tools](https://dash.plotly.com/devtools).

**Servindo a aplicação em dash como versão para teste**

```python
if __name__ == '__main__':
    app.run(debug=True, port=1, use_reloader = False)

# port=1 irá servir a aplicação na porta 1, a qual por padrão é a porta 8050
```

O exemplo acima deve ser salvo como um arquivo Python (extensão ".py") e ser executado usando

> `python [nome do arquivo].py`.

>`app.run(debug = True, use_reloader = False)`.

* use_reloader=True (padrão):

    Quando debug=True, o Dash automaticamente ativa o "reloader". Isso faz com que:

    - O servidor seja executado duas vezes ao iniciar:

        - Uma instância principal

        - Uma instância "escondida" que fica monitorando alterações no código

    - Ao detectar qualquer mudança no script (.py), o servidor é automaticamente reiniciado.

* use_reloader=False:

    - Impede a duplicação de execução ao iniciar o servidor.

    - Evita confusão em ambientes onde o código não pode ser duplicado (como notebooks, Jupyter, VSCode interactive, ou sistemas com side-effects na inicialização).

## **CallBack**

CallBack é uma função de chamada que compõe as aplicações com Dash. Essa é responsável por deixar a aplicação interativa e promover a atualização automática de funções assim que as propriedades de entrada (*input*) a essas são alteradas.

Em qualquer atributo, seja ele criado com `dash_core_components` ou `dash_html_components`, os parametos criados são do tipo `style`, `className`, `id` e etc. Esses parâmetros, especialmente o parametro `id`, axiliam a callback uma vez que identifica um certo componente (não é possível ter um mesmo `id` para dois componentes).

Encontre mais exemplos sobre callback em [Basic CallBacks](https://dash.plotly.com/basic-callbacks).

### **Segundo Exemplo - `Exemplo_2.py`**
O código desenvolvido e comentado está na pasta [Exercicios](\Exercicios)


Para esse exemplo, foram utilizados os seguintes componentes:
* `dcc.Tabs`
* `dcc.Tab`
* `go.Scatter` e `go.Bar` da biblioteca `plotly.graph_objects`, funções muito utilizadas para visualização de dados em gráfico.

#### **Importando os módulos necessários**

```python
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
```

#### **Ajustando o tipo de fonte usando CSS para modificar o padrão dos elementos utilizados e criando o aplicativo com a função `Dash()` da biblioteca Dash.**

```python
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app2 = dash.Dash(__name__, external_stylesheets=external_stylesheets)
```

Com aplicativos Dash mais complexos que envolvem modificação dinâmica do layout (como [Multi-Page Apps](https://dash.plotly.com/urls)), nem todos os componentes que aparecem em seus retornos de chamada serão incluídos no layout inicial. Você pode remover essa restrição desativando a validação de retorno de chamada:
> `app.config.suppress_callback_exceptions = True`

Nesse exemplo, todas os componentes aparecem na mesma callback e não utilizamos modificação dinâmica de layout. Portanto, não é necessário suprimir as exceções.

#### **Construindo o layout do app2**

```python
app2.layout = html.Div(
    [
        html.H2(
            ['Painel de visualização de gráficos'],
            style={
                'textAlign':'center',
                'font-weight':'bold'
                }
        ),

        html.Hr(),

        dcc.Tabs(
            id='tabs',
            children=[
                dcc.Tab(label='Gráfico de linha',value='tab-1'),
                dcc.Tab(label='Gráfico de Barra',value='tab-2'),
                dcc.Tab(label='Gráfico de Linha e Pontos',value='tab-3')
            ]
        ),
        html.Div(id='tabs-content'),

        html.Hr(),
    ]
)
```

#### **Função de apoio criada para retornar o gráfico gerado em cada aba**

```python
def gera_grafico(tipo):
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[0,1,2,3,4,5,6],
            y=[0,1,2,3,4,5,6],
            mode=tipo,
            name='Reta',
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[0,1,2,3,4,5,6],
            y=[0,1,4,9,16,25,36],
            mode=tipo,
            name='Parábola',
            )
        )

    fig.update_layout(title='Gráfico Exemplo')
    
    return fig
```

#### **Construindo o `@app2.callback()`**

```python
@app2.callback(
    Output('tabs-content','children'),
    [
        Input('tabs','value')
    ]
)
def update_tab(tab):

    if tab == 'tab-1':
        return html.Div(
            [
                dcc.Graph(
                    figure = gera_grafico('lines')
                )
            ]
        )

    elif tab == 'tab-2':

        fig_bar = go.Figure()

        fig_bar.add_trace(
            go.Bar(
                x=[0,1,2,3,4,5,6],
                y=[0,1,2,3,4,5,6],
                )
            )

        fig_bar.add_trace(
            go.Bar(
                x=[0,1,2,3,4,5,6],
                y=[0,1,4,9,16,25,36],
                )
            )
        fig_bar.update_layout(title='Gráfico em Barras Exemplo')
        
        return html.Div(
            [
                dcc.Graph(
                    figure = fig_bar
                )
            ]
        )

    elif tab == 'tab-3':
        
        return html.Div(
            [
                dcc.Graph(
                    figure = gera_grafico('lines+markers')
                )
            ]
        )

    else:
        return html.Div(
            ['Erro 404']
        )
```

#### **`Input` e `Output` são os responsáveis pelas alterações automáticas na interface da aplicação web.**

**Servindo a aplicação em dash como versão para teste**

```python
if __name__ == "__main__":
    app2.run(debug=True, port=2, use_reloader=False)
```

O exemplo acima deve ser salvo como um arquivo Python (extensão ".py") e ser executado usando

> `python [nome do arquivo].py`.

>`app.run(debug = True, use_reloader = False)`.

## **Dash Core Components**

Este pacote fornece o pacote principal de componentes React para Dash.

### **Prévia dos componentes**
* [Overview Dash Core Components](https://dash.plotly.com/dash-core-components)

### **Dropdown**

* [Dropdown Examples and Reference](https://dash.plotly.com/dash-core-components/dropdown)

```python
# estrutura simplificada
dcc.Dropdown(
        options=[
            {
                'label': f'Opção {value}', 'value': f'{value}'
            }
            for value in range(0,10)
        ],
        value='Opção 1'
    ),

# estrutura padrão
dcc.Dropdown(
        options=[
            {'label': f'Opção 1', 'value': '1'},
            {'label': f'Opção 2', 'value': '2'},
            {'label': f'Opção 3', 'value': '3'},
        ],
        value='Opção 1'
    ),
```

### **Slider**

Esse componente funciona como um controle deslizante muito utilizado para gráficos em que é possível aumentar ou diminuir a amplitude de valores de um determinando eixo.
* [Slider Examples and Reference](https://dash.plotly.com/dash-core-components/slider)

```python
dcc.Slider(
    min=-5,
    max=10,
    step=0.5,
    value=-3
)
```

### **RangeSlider**
Esse funciona de forma semelhante ao componente acima, porém com o RangeSlider é possível realizar esse controle através das duas extremidades do componente.
* [RangeSlider Examples and Reference](https://dash.plotly.com/dash-core-components/rangeslider).

```python
dcc.RangeSlider(
    count=1,
    min=-5,
    max=10,
    step=0.5,
    value=[-3, 7]
)
```

### **Input**
* [Input Examples and Reference](https://dash.plotly.com/dash-core-components/input)

```python
dcc.Input(
    placeholder='Enter a value...',
    type='text',
    value=''
)
```

### **Checkboxes**

São caixas de seleção em que é possível receber informações.
* [dcc.Checklist](https://dash.plotly.com/dash-core-components/checklist)

```python
# estrutura simplificada
dcc.Checklist(
    options=[
        {
            'label': f'Opção {value}', 'value': f'{value}'
        }
        for value in range(0,10)
    ],
    value='Opção 1'
)

# estrutura padrão
dcc.Checklist(
    options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montréal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
    value=['MTL', 'SF']
)
```

### **Radio Items**
* [dcc.RadioItems Examples & Documentation](https://dash.plotly.com/dash-core-components/radioitems)

```python
# estrutura simplificada
dcc.RadioItems(
    options=[
        {
            'label': f'Opção {value}', 'value': f'{value}'
        }
        for value in range(0,10)
    ],
    value='Opção 1'
)

# estrutura padrão
dcc.RadioItems(
    options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montréal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
    value='MTL'
)
```

### **Graph**

O componente `dcc.Graph` compartilha da mesma sintaxe da biblioteca _plotly.py_, ou seja, a construção do que o parâmetro _figure_ recebe é semelhante (data,layout,...).

É possível passar as informações do gráfico em forma de dícionário como apresentado abaixo ou atribuindo ao parâmetro _figure_ uma figura já criada com a biblioteca plotly.py.

* [dcc.Graph](https://dash.plotly.com/dash-core-components/graph)

```python
dcc.Graph(
    id='example-graph',
    figure={
        'data':[
                {'x':[0,1,2,3,4,5,6],'y':[0,1,2,3,4,5,6],'type':'line+markers','name':'Reta'},
                {'x':[0,1,2,3,4,5,6],'y':[0,1,4,9,16,25,36],'type':'line+markers','name':'Parábola'}
        ],
        'layout':{
            'title':'Gráfico Exemplo'
        }
    }
)
```

### **Link**

* [dcc.Link](https://dash.plotly.com/dash-core-components/link)

```python
dcc.Link('Ir para outra página', href='/pagina-exemplo'),
dcc.Link('Acesse o site', href='https://example.com')
```

### **Visualização dos Componentes - `dash_core.py`**
O código desenvolvido e comentado está na pasta [Exercicios](\Exercicios)

```python
import dash
from dash import dcc, html
```

```python
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app_dash_core_components = dash.Dash(__name__, external_stylesheets=external_stylesheets)
```

```python
app_dash_core_components.layout = html.Div(
    [
        html.H1(
            'Dash Core Components',
            style={
                'textAlign':'center',
                'font-weight':'bold'
            }
        ),

        html.Div(
            [
                html.Hr(),

                html.H2(
                    ['Componente Dropdown']
                ),

                dcc.Dropdown(
                    options=[
                        {
                            'label': f'Opção {value}', 'value': f'{value}'
                        }
                        for value in range(0,10)
                    ],
                    value='1'
                ),

                html.Hr(),

                html.H2(
                    ['Componente Slider']
                ),
        
                dcc.Slider(
                    min=-5,
                    max=10,
                    step=0.5,
                    value=-3
                ),

                html.Hr(),

                html.H2(
                    ['Componente RangeSlider']
                ),

                dcc.RangeSlider(
                    count=1,
                    min=-5,
                    max=10,
                    step=0.5,
                    value=[-3, 7]
                ),

                html.Hr(),

                html.H2(
                    ['Componente Input']
                ),

                dcc.Input(
                    placeholder='Insira uma mensagem...',
                    type='text',
                    value=''
                ),
                
                html.Hr(),
                html.H2(
                    ['Componente Link']
                ),

                dcc.Link('Acesse o site', href='https://github.com/Grupo-EngePol/EngeData-Monitoring'),

            ],
            style={
                'margin-left':'10px',
                'margin-right':'10px',
                'width': '48%',
                'display':'inline-block',
                'float':'left',
                'border': '2px solid lightblue'
            }
        ),

        html.Div(
            [
                html.Hr(),

                html.H2(
                    ['Componente Checklist']
                ),

                dcc.Checklist(
                    options=[
                        {
                            'label': f'Opção {value}', 'value': f'{value}'
                        }
                    for value in range(1,6)
                    ],
                    value=['1', '9']
                ),

                html.Hr(),

                html.H2(
                    ['Componente RadioItems']
                ),

                dcc.RadioItems(
                    options=[
                        {
                            'label': f'Opção {value}', 'value': f'{value}'
                        }
                        for value in range(1,6)
                    ],
                    value='MTL'
                ),

                html.Hr(),

                html.H2(
                    ['Componente Graph']
                ),

                dcc.Graph(
                    id='example-graph',
                    figure={
                        'data':[
                                {'x':[0,1,2,3,4,5,6],'y':[0,1,2,3,4,5,6],'type':'line+markers','name':'Reta'},
                                {'x':[0,1,2,3,4,5,6],'y':[0,1,4,9,16,25,36],'type':'line+markers','name':'Parábola'}
                        ],
                        'layout':{
                            'title':'Gráfico Exemplo'
                        }
                    }
                ),
            ],
            style={
                'margin-left':'10px',
                'margin-right':'10px',
                'width': '48%',
                'display':'inline-block',
                'float':'right',
                'border': '2px solid lightblue'
                }
        )

    ],
    style={
        'margin-left':'10px',
        'margin-right':'10px',
        'border': '2px solid lightblue'
    }
)
```

```python
if __name__ == "__main__":
    app_dash_core_components.run(debug=True, port=3, use_reloader=False)
```

## **Dash HTML Components**

Em vez da escrita em HTML ou de utilizar templates com HTML, você pode construir seu layout usando Python puro para desenvolver as mesmas funções com a biblioteca `dash_html_components`.

### **Prévia dos componentes**
* [Overview Dash HTML Components](https://dash.plotly.com/dash-html-components)

### **html.Div**

* [html.Div](https://dash.plotly.com/dash-html-components/div).

É bastante utilizado para alocar outros componentes. Pensando no compontente html.Div como uma caixa, tem-se ele para armazenar algo, ou seja, uma divisão destinada a algo.

```python
html.Div(
    children=['Parâmetro principal'],
    id='',
    className='',
    style={},
    n_clicks=0, #default
)
```

### **html.H1 - html.H2 - html.H3 - html.H4 - html.H5 - html.H6**

Para trabalhar com a propriedade *style* e *className* dos componentes hmtl e dcc, esse [site](https://www.w3schools.com/css/default.asp) fornece dicas de CSS, linguagem de marcação utilizada para adicionar estilo em documentos HTML.

```python
html.H1(
    children=[],
    id='',
    className='',
    style={},
    n_clicks=0, #default
)
```

#### **html.P**

* [html.P]().

Elemento paragráfo/bloco indentado do texto.

```python
htlm.P(
    children=[],
    id='',
    className='',
    style={}
)
```

### **html.Button**

* [Button Examples and Reference](https://dash.plotly.com/dash-html-components/button).

```python
html.Button(
    children=[],
    id='',
    className='',
    n_clicks=0, #default
    n_clicks_timestamp= -1, #default
)
```

### **html.Hr**

* [html.Hr](https://dash.plotly.com/dash-html-components/hr).

Fornece uma linha horizontal.

Quando é utilizado `dcc.Markdown`, podemos inserir essa linha com "" ou "___" sem a necessidade de inserir um componente `html.Hr()`.

```python
html.Hr(
    children=[],
    id='',
    className='',
)
```

#### **html.Table - html.Th - html.Td**

De forma semelhante ao que é entregue utilizando a biblioteca Dash Table, com esses componentes utilizados em conjunto é possível construtir quadros para a apresentação de dados em forma de tabela.

_Recomendo estudar a biblioteca _dash_table_, pois com ela é fácil de apresentar dados de forma mais interativa e dinâmica._

* [html.Table](https://dash.plotly.com/dash-html-components/table)
* [html.Th](https://dash.plotly.com/dash-html-components/th)
* [html.Td](https://dash.plotly.com/dash-html-components/td)

```python
html.Table(
    [
        html.Tr(
            [
                html.Th('1'),
                html.Th('2'),
                html.Th('3'),
                html.Th('4')
            ]
        ),
        html.Tr(
            [
                html.Td('a11'),
                html.Td('a12'),
                html.Td('a13'),
                html.Td('a14')
            ]
        ),
        html.Tr(
            [
                html.Td('a21'),
                html.Td('a22'),
                html.Td('a23'),
                html.Td('a24')
            ]
        ),
    ]
)
```

#### Exemplo de função para apresentação de dados de um _dataframe_ em forma de quadro usando componentes do tipo `dash_html_componentes`

```python
def gera_planilha(dataframe): 

    return html.Table(
        [
            # colunas
            html.Thead(
                html.Tr(
                    [
                        html.Th(col) for col in dataframe.columns
                    ]
                )
            ),
            # dados
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(
                                dataframe.iloc[i][col]
                            )
                            for col in dataframe.columns
                        ]
                    )
                    for i in range(len(dataframe))
                ]
            )
        ]
    )
```

## **Dash DataTable**

Dash DataTable é um componente interativo em tabela que serve para visualização e edição de dados com Python.

* [Dash DataTable](https://dash.plotly.com/datatable)

Para demonstrar a função `dash_table.DataTable()` dessa biblioteca, utilizei o arquivo `sousa_geral_anual.csv` que está dentro da pasta codigos_videos.


### Dash DataTable - `Exemplo_3.py`
O código desenvolvido e comentado está na pasta [Exercicios](\Exercicios)

Para esse exemplo, não foi criada uma função chamada `gera_tabela(df)` com a função de retornar a tabela para a minha aplicação web. Entretanto, deixei uma função abaixo que ao receber um _dataframe_ retorna a tabela com os dados.

Links de apoio:
* [Dash DataTable - Styling](https://dash.plotly.com/datatable/style).
* [Dash DataTable - Interactivity](https://dash.plotly.com/datatable/interactivity).
* [Editable DataTable](https://dash.plotly.com/datatable/editable).

#### **Importando `dash_table`**

```python
import dash
import pandas as pd
from dash import dash_table, html
```

```python
df = pd.read_csv('sousa_geral_anual.csv')

app3 = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1('Tabela de dados da cidade de Sousa - PB'),

        dash_table.DataTable(

            # dados
            data= df.to_dict('records'),

            # identificação das colunas da planilha
            columns=[
                {
                    'name': col,
                    'id': col
                }
                for col in df.columns
            ],

        )
    ]
)
```

```python
if __name__ == '__main__':
    app3.run(debug=True, use_reloader=False)
```

É uma boa prática gerar uma função para retornar o quadro de dados quando a aplicação for redenrizada no navegador.

```python
def gera_tabela(df):

    return dash_table.DataTable(

            data = df.to_dict('records'),

            columns = [
                {
                    'name': col, 
                    'id': col,
                } 
                for col in df.columns
            ],

            style_cell={
                'textAlign': 'center',
                'border': '1px solid grey',
                'minWidth':'90px',
                'width':'125px',
                'maxWidth':'160px',
                'fontSize':'14',
                'font-family':'sans-serif'
                },
                
            style_header={
                'backgroundColor': '#ADD8E6',
                'fontWeight': 'bold'
            },

            page_size = 12,

            style_table = {
                'height':'auto',
                'minWidth': '100%',
                'overflowX': 'auto',
                'border': '2px solid lightgreen',
            }
        )
```

## Construção de um Mini Dashboard com Dash em Python - `Exemplo_cidade_sousa.py`
O código desenvolvido e comentado está na pasta [Exercicios](\Exercicios)

Para criação dessa apicação com Dash, utilizei o arquivo `sousa_geral_anual.csv` que está dentro da pasta codigos_videos.

```python
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
```

Funções de Apoio para construção do Layout e para a manipulação dos dados do arquivo `sousa_geral_anual.csv`

```python
def gera_tabela(df):

    return dash_table.DataTable(

            # dados
            data = df.to_dict('records'),

            # colunas
            columns = [
                {
                    'name': col, 
                    'id': col,
                } 
                for col in df.columns
            ], 
            
            style_cell={
                'textAlign': 'center',
                'border': '1px solid grey',
                'minWidth':'90px',
                'width':'125px',
                'maxWidth':'160px',
                'fontSize':'14',
                'font-family':'sans-serif'
                },
                
            style_header={
                'backgroundColor': '#8FBC8F',
                'fontWeight': 'bold'
            },

            page_size = 16,

            style_table = {
                'height':'auto',
                'minWidth': '100%',
                'overflowX': 'auto',
                'border': '2px solid lightgreen',
            }
        )

# essa função está renomeando as colunas de um dataframe pelos nomes presentes na lista
def gera_dados_selec(df):
    list_colunas = [
        'Tempo','Precipitação Média','Umidade a 2m','Umidade Relativa a 2m (%)','Pressão na Superfície (kPa)',
        'Média das Temp. a 2m (°C)','Média das Temp. Mínimas a 2m (°C)','Média das Temp. Máximas a 2m (°C)',
        'Média das Vel. Mínimas do Vento a 50m (m/s)','Média das Vel. Mínimas do Vento a 10m (m/s)',
        'Média das Vel. Máximas do Vento a 50m (m/s)','Média das Vel. Máximas do Vento a 10m (m/s)',
        'Média das Vel. do Vento a 50m (m/s)','Média das Vel. do Vento a 10m (m/s)','Temp. Máxima a 2m (°C)',
        'Média das Vel. do Vento a 50m (m/s)','Vel. Máxima do Vento a 10m (m/s)','Temp. Mínima a 2m (°C)',
         'Vel. Mínima do Vento a 50m (m/s)','Vel. Mínima do Vento a 10m (m/s)','Precipitação Acumulada'
    ]
    df.columns = map(lambda x: x.title(),list_colunas)

    return df

# criando o cabeçalho para facilitar na construção do layout
def div_topo():
    return html.Div(
        children=[
            html.H2(
                'Informações da Cidade de Sousa-PB',
                style={'font-weight':'bold',}
            ),

            html.H4('Dados de 1983 até 2018')
        ],
        style={
            'textAlign':'center',
            'font-weight':'bold',
            'border': '2px solid lightgreen',
            'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
            'background-color':'#8FBC8F',
            }
    )

# criando o rodapé para facilitar na construção do layout
def div_base():
    return html.Div(
        children=[
            dcc.Markdown(''' ### **Sousa, Paraíba - 2020**'''),

            dcc.Markdown('''#### Site: [Cidade Sousa](https://www.sousa.pb.gov.br/)''')
        ],
        style={
            'textAlign':'center',
            'font-weight':'bold',
            'border': '2px solid lightgreen',
            'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
            'background-color':'#8FBC8F',
            }
    )
```

```python
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets
)

df = gera_dados_selec(pd.read_csv('sousa_geral_anual.csv'))

colunas = list(df.columns)
```

```python
app.layout = html.Div(
    [
        div_topo(),

        html.H4(
            ['Selecione os Dados:'],
            style={
                'textAlign':'justify',
                'text-indent': '50px',
                'line-height': '3'
                }
        ),

        # parte central do layout
        html.Div(
            [
                # bloco esquerdo da parte central do layout
                html.Div(
                    [
                        dcc.Dropdown(
                            # nome do componente
                            id='columns',
                            # lista de opções
                            options=[
                                {
                                    'label': i,
                                    'value': i
                                }
                                for i in colunas[1:]
                            ],
                            value='Precipitação Média'
                        ),

                        html.Hr(),

                        dcc.Graph(
                            id='indicator-graphic',
                            style={'border': '2px solid lightgreen','background-color':'#ADD8E6'}
                        ),
                    ],
                    style={'margin-left': '15px','width':'48%', 'display':'inline-block'}
                ),

                # bloco direito da parte central do layout
                html.Div(
                    [
                        gera_tabela(df),
                    ],
                    style={'margin-right': '15px','width':'48%', 'float': 'right', 'display':'inline-block'}
                )
            ]
        ),

        html.Hr(),

        div_base()

    ],
    style={
        'border': '2px solid lightgreen'
        ,'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'
        ,'background-color':'#90EE90'
    }
)
```

```python
@app.callback(
    Output('indicator-graphic','figure'),
    [
        Input('columns','value'),
    ]
)
def update_graph(coluna):

    return{
        # dados (uma chave contendum dicionário com informações do gráfico)
        'data':[
            dict(
                x=df['Tempo'],
                y=df[str(coluna)],
                mode='lines+markers',
                text=str(coluna),
                opacity=0.8
            )
        ],
        'layout': dict(
            xaxis={
                'title':'Anual',
                'type':'date',
                'rangeslider': 'dict(visible=True)'
            },
            yaxis={
                'title':coluna,
                'type':'linear'
            },
            margin={'l': 100, 'b': 40, 't': 40, 'r': 100},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
```

```python
if __name__ == '__main__':
    app.run(debug=True)
```
