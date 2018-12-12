#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, cgi

print """
<!DOCTYPE html>
<html>
<head>
<title>map</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta charset="utf-8" />

  <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.4/dist/leaflet.css"
  integrity="sha512-puBpdR0798OZvTTbP4A8Ix/l+A4dHDD0DGqYW6RQ+9jxkRFclaxxQb/SJAWZfWAkuyeQUytO7+7N4QKrDh+drA=="
  crossorigin=""/>
  <link rel="stylesheet" href="../node_modules/leaflet-sidebar-v2/css/leaflet-sidebar.css" />

  <script src="https://unpkg.com/leaflet@1.3.4/dist/leaflet.js"
  integrity="sha512-nMMmRyTVoLYqjP9hrbed9S+FzjZHW5gY1TWCHA5ckwXZBadntCNs8kEqAWdrb9O7rxbCaA4lKTIWjDXZxflOcA=="
  crossorigin=""></script>
  <!-- script src="http://code.jquery.com/jquery-1.10.1.min.js"></script-->
  <script src="../node_modules/betterwms/L.TileLayer.BetterWMS.js"></script>
  <script src="../node_modules/leaflet-sidebar-v2/js/leaflet-sidebar.js"></script>


  <style>
      body {
          padding: 0;
          margin: 0;
      }

      html, body, #map {
          height: 100%;
          font: 10pt "Helvetica Neue", Arial, Helvetica, sans-serif;
      }

      .lorem {
          font-style: italic;
          color: #AAA;
      }
  </style>

</head>
<body>

<!-- Barra lateral -->
  <div id="sidebar"  class="sidebar collapsed" >

        <!-- Nav tabs -->
        <div class="sidebar-tabs">
            <ul role="tablist">
                <li><a href="#home" role="tab"><i class="fa fa-bars"></i></a></li>
                <li><a href="#settings" role="tab"><i class="fa fa-gear"></i></a></li>
                <li><a href="#messages" role="tab"><i class="fa fa-envelope"></i></a></li>
                <li><a href="https://github.com/marcianolima" role="tab" target="_blank"><i class="fa fa-github"></i></a></li>
            </ul>
            <ul role="tablist">
                <li class="disabled"><a href="#profile" role="tab"><i class="fa fa-user"></i></a></li>
            </ul>
        </div>


        <div class="sidebar-content">
            <div class="sidebar-pane" id="home">
                <h1 class="sidebar-header">
                    Sobre
                    <span class="sidebar-close"><i class="fa fa-caret-left"></i></span>
                </h1>

                <p>Projeto Disciplina Desenvolvimento de Aplicações Geoespaciais</p>

                <p class="lorem">Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>
            </div>

            <div class="sidebar-pane" id="settings">
                <h1 class="sidebar-header">Criar Pirâmide Raster: <span class="sidebar-close"><i class="fa fa-caret-left"></i></span></h1>

                <form>

                 Insira a imagem:<br>
                 <input type="file" name="myRaster"><br>
                 <!--
                 Escreva o caminho da imagem:<br>
                <input type="text" name="dirRaster"><br>
                -->
                 Numero de niveis de reamostragem:
                  <select name="levels">
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4</option>
                  <option value="5">5</option>
                  <option value="6">6</option>
                  <option value="7">7</option>
                  <option value="8">8</option>
                  <option value="9">9</option>
                  <option value="10">10</option>
                  </select><br>

                 Escolha o tamanho da tile:
                 <select name="tileSize">
                 <option value="256">256 X 256</option>
                 <option value="512">512 X 512</option>
                 <option value="1024">1024 X 1024</option>
                 <option value="2048">2048 X 2048</option>
                 </select><br>

                 Escolha a dimensao de pixel das tiles:
                 <select name="pixelSize">
                 <option value="128">128</option>
                 <option value="256">256</option>
                 <option value="512">512</option>
                 <option value="1024">1024</option>
                 <option value="2048">2048</option>
                 <option value="3072">3072</option>
                 <option value="4096">4096</option>
                 <option value="5120">5120</option>
                 <option value="6144">6144</option>
                 </select><br>

                 Digite o numero da projecao (EPSG):<br>
                 <input type="text" name="epsg"><br>

                 Digite um nome para a pasta de destino:<br>
                 <input type="text" name="dirName"><br>

                 <button onclick="myFunction()">Criar Piramide</button>

                <script>
                function myFunction() {
                    var x = document.getElementById("myRaster");
                    x.disabled = true;
                }
                </script>"""

form = cgi.FieldStorage()

myRaster =  form.getvalue('myRaster')
#localRaster =  form.getvalue('localRaster')
levels =  form.getvalue('levels')
tileSize =  form.getvalue('tileSize')
pixelSize =  form.getvalue('pixelSize')
epsg =  form.getvalue('epsg')
dirName =  form.getvalue('dirName')

if dirName != None:
    dir = './%s'%dirName
    os.makedirs(dir)
    gdalRetile = """gdal_retile.py -v -r bilinear -levels %i -ps %i %i -co "TILED=YES" -co "BLOCKXSIZE=%i" -co "BLOCKYSIZE=%i" -s_srs EPSG:%i -targetDir %s .\/raster\/%s""" %(int(levels), int(pixelSize), int(pixelSize), int(tileSize), int(tileSize), int(epsg), str(dir), str(myRaster))
    os.system(gdalRetile)


print """
               </form>

            </div>

            <div class="sidebar-pane" id="messages">
                <h1 class="sidebar-header">Mensagem<span class="sidebar-close"><i class="fa fa-caret-left"></i></span></h1>
                <p>Dúvidas, sugestões, ajuda: <a href="mailto:marcianodacostalima@gmail.com" target="_top">marcianodacostalima@gmail.com</a></p>
            </div>

            <div class="sidebar-pane" id="profile">
                <h1 class="sidebar-header">Settings<span class="sidebar-close"><i class="fa fa-caret-left"></i></span></h1>
            </div>
        </div>
</div>



  <!-- Mapa leaflet -->
  <div id='map' class="sidebar-map" ></div>



  <script>
  var mymap = L.map('map').setView([-25.4505,-49.2350], 15);

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery <a href="https://www.mapbox.com/">Mapbox</a>, Sidebar V2 <a href="https://github.com/Turbo87/sidebar-v2">Github</a>',
    maxZoom: 23,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibWFyY2lhbm9kYWNvc3RhbGltYSIsImEiOiJjamV5eGsxZ3IwNGFrMndxb216dWwwenB1In0.maLUDU8v7Xi5PAOkjzPwMg'
  }).addTo(mymap);

  var poliPyramid15cm = L.tileLayer.wms('https://mapas.geomatica.ufpr.br/geoserver/CampusMap/wms', {
    layers: 'CampusMap:pyramid15cm', transparent: 'true', format: 'image/png',
    maxZoom: 23
  }).addTo(mymap);

  var poliPyramid5cm = L.tileLayer.wms('https://mapas.geomatica.ufpr.br/geoserver/CampusMap/wms', {
    layers: 'CampusMap:pyramid5cm', transparent: 'true', format: 'image/png',
    maxZoom: 23
  });

  var poliEdificio = L.tileLayer.wms('https://mapas.geomatica.ufpr.br/geoserver/CampusMap/wms', {
    layers: 'CampusMap:edificio', transparent: 'true', format: 'image/png',
    maxZoom: 23
  });

  var poliEsquematico = L.tileLayer.wms('https://mapas.geomatica.ufpr.br/geoserver/CampusMap/wms', {
    layers: 'CampusMap:esquematico', transparent: 'true', format: 'image/png',
    maxZoom: 23
  });


//layers localhost

  var poliLimite = L.tileLayer.wms('http://localhost:8080/geoserver/teste/wms', {
    layers: 'teste:limite_politecnico', transparent: 'true', format: 'image/png', styles: 'teste:azul',
    maxZoom: 23
  }).addTo(mymap);

  var poli1000 = L.tileLayer.wms('http://localhost:8080/geoserver/teste/wms', {
    layers: 'teste:politecnico_escala_1000', transparent: 'true', format: 'image/png', styles: 'teste:vermelho',
    maxZoom: 23
  });

  var poli500 = L.tileLayer.wms('http://localhost:8080/geoserver/teste/wms', {
    layers: 'teste:politecnico_escala_500', transparent: 'true', format: 'image/png', styles: 'teste:verde',
    maxZoom: 23
  });

  var poli250 = L.tileLayer.wms('http://localhost:8080/geoserver/teste/wms', {
    layers: 'teste:politecnico_escala_250', transparent: 'true', format: 'image/png', styles: 'teste:lilas',
    maxZoom: 23
  });

//criando controle de layers

  var baseLayers = {
    "Piramide 15 cm CampusMap": poliPyramid15cm,
    "Piramide 5 cm CampusMap": poliPyramid5cm
  };

  var overlays = {
    "Mapa Edificios": poliEdificio,
    "Limite Politecnico": poliLimite,
    "Articulacao 1:1000": poli1000,
    "Articulacao 1:500": poli500,
    "Articulacao 1:250": poli250,
    "Mapa Esquematico": poliEsquematico
  };

  L.control.layers(baseLayers, overlays,{collapsed:false}).addTo(mymap);


  var sidebar = L.control.sidebar('sidebar').addTo(mymap);
  </script>

</body>
</html>
"""
