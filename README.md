# biojor_car_eduardo


Para baixar os dados, copiar pasta "dados" no drive inteira e colocar ela na pasta pasta base do projeto. 



Para baixar pacotes python usados:

Com conda : conda env create -f environment.yml


Com pip : pip install -r requirements.txt



Contém:
    Exemplo.v0 : Aquele jupyter inicial que mandei no slack.
    Car_interseção: Jupyter que encontra interseção de C.A.Rs, ou seja registros que se sobrepõe e gera tabela de resultados.
    Car_UC: Jupyter para encontrar C.A.R em cima de U.Cs e exportar dados em uma tabela , analise por UC
    analise_completa: Codigo  .py (por questões de perfomance) para fazer a analise por municipio, considerando toda as categorias e exportar dados (opcionalmente plota aquelas interseções que mandei no slack e o mapa com todas em pdf (demora um pouco!) )

    dados: Shapefiles: C.A.Rs do Pará, UCs, TIs, Quilombolas, FPND e Assemantas do Brasil e ja filtrados para o Pará. Municipios e limites estaduais do Pará.

    
    obs: Cometários feito por I.A.