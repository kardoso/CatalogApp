## Requerimentos
- [Python 3](https://www.python.org/downloads/release/python-371/)
- [SQLAlchemy](https://www.sqlalchemy.org/) - Use o comando `pip install sqlalchemy` para instalar
- [Flask](http://flask.pocoo.org) - Use o comando `pip install Flask` para instalar
- [httplib2](https://github.com/httplib2/httplib2) - Use o comando `pip install httplib2` para instalar
- [oauth2client](https://github.com/googleapis/oauth2client) - Use o comando `pip install --upgrade oauth2client` para instalar
#### Caso prefira executar em um ambiente virtual utilize a máquina virtual vagrant:
- [Vagrant](https://www.vagrantup.com) - Ambiente de desenvolvimento - 
Baixe o arquivo com a máquina configurada [aqui](https://d17h27t6h515a5.cloudfront.net/topher/2017/June/5948287e_fsnd-virtual-machine/fsnd-virtual-machine.zip)
- [Virtual Box](https://www.virtualbox.org/wiki/Downloads) - Para rodar a VM vagrant

É recomendado utilizar a máquina virtual como ambiente de desenvolvimento, 
mas caso prefira executar na própria máquina não é necessário instalar o virtualbox, nem baixar o vagrant.


## Prepare o ambiente
### Caso tenha optado pela virtualização
Instale o Virtual Box

Descomprima o arquivo da VM Vagrant

Coloque os arquivos dentro da pasta `vagrant` do arquivo baixado.

Com a pasta vagrant aberta em um terminal insira o comando `vagrant up` para ligar a máquina virtual, em seguida o comando
`vagrant ssh` para fazer o login na máquina.

Vá até a pasta compartilhada com o comando `cd /vagrant`.


## Execute o servidor
Execute o arquivo `initdb.py` para criar o banco de dados e configurá-lo já com alguns itens.
No terminal use o comando `python initdb.py` ou `python3 initdb.py` se tiver mais de uma versão do python instalada.

Depois de montar o banco de dados execute o arquivo `app.py` com o comando `python app.py`

O aplicativo estará rodando e poderá ser acessado a partir da url `localhost:8000`


## Caminhos do site
O site possui quatro(4) páginas apenas, destinadas ao index(mostrar todos os itens), mostrar itens específicos, criar itens e editar itens.
A exclusão de itens é feita na própria página específica do item.

Caminhos possíveis                   |Página                                             
-------------------------------------|---------------------------------------------------
`/`, `/catalog` ou `/catalog.html`   |Página principal mostrando os 3 itens mais recentes
`/catalog?category=vehicles`         |Página principal mostrando todos os itens da categoria `vehicles` 
`/item?id=1` ou `/item.html?id=1`    |Acessa a página do item cujo id é 1                        
`/create` ou `/create.html`          |Página de criação de itens       
`/edit?item=3` ou `/edit.html?item=3`|Página de edição do item cujo id é 3 

As páginas de criação e edição só podem ser acessadas por quem está logado.
E a exclusão de itens também só pode ser feita por quem está logado.

O login é feito a partir da conta google.

**Obs**: Utilize a url localhost:8000 para ter acesso ao login do google.


## Endpoints JSON - API
O app possui endpoints públicas no formato json.
Como utilizar a API:

Caminho                    |Função                                             
---------------------------|---------------------------------------------------
/catalog.json              |Mostra todas as categorias e seus respectivos itens
/categories.json           |Mostra apenas as categorias                        
/category.json?name=clothes|Mostra todos os itens da categoria `clothes`       
/item.json?id=1            |Mostra as informações do item cujo id é 1          
