#import pour les infos meteo
#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8#coding=utf-8#coding=utf-8#coding=utf-8
import os.path
import urllib2
import json
import sys

import time
from daemon import runner

#=========================================================== 
#       La classe
#===========================================================        

class App(): 
    
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null' 
        self.stderr_path = '/dev/null' 
        self.pidfile_path = '/tmp/meteo.pid'
        self.pidfile_timeout = 5
    
   
    def run(self): 
    
        
        while True: 
        
            ###############################################
            #           Le corps du programme             #
            ###############################################
            try:
           
        
            # Je charge ma page meteo
                page_json = urllib2.urlopen('http://api.wunderground.com/api/macleapi/forecast/conditions/lang:FR/q/France/Paris.json?paris=I75003PA1')
                # Je lis la page
                json_string = page_json.read()
                # Je mets cette page dans un parseur
                parsed_json = json.loads(json_string)
                # Et je peux fermer ma page meteo, je n'en ai plus besoin
                page_json.close()
            except: 
                print 'Les informations ne sont pas accessibles sur le site wunderground.com' 
                sys.exit(2)


            city = parsed_json['current_observation']['display_location']['city'] # la ville
            last_observation = parsed_json['current_observation']['observation_time'] 
            current_temp = parsed_json['current_observation']['temp_c'] # la 
            current_weather = parsed_json['current_observation']['weather'] # le temps actuel
            humidity = parsed_json['current_observation']['relative_humidity'] # 
            wind_kph = parsed_json['current_observation']['wind_kph'] # la vitesse du vent
            wind_dir = parsed_json['current_observation']['wind_dir'] #
            pressure_mb = parsed_json['current_observation']['pressure_mb'] 
            pressure_trend = parsed_json['current_observation']['pressure_trend'] # 
            feelslike_c = parsed_json['current_observation']['feelslike_c'] # 
            visibility = parsed_json['current_observation']['visibility_km'] # 
            UV = parsed_json['current_observation']['UV'] # l'indice UV
            print 'sur le site wunderground.com' + city
            
            if str(UV) == '-1':
                UV = 0
            
           
            
            if pressure_trend == '-':
                pressure_trend = 'en baisse'
            elif pressure_trend == '+':
                pressure_trend = 'en hausse'
            else:
                pressure_trend = 'stable'
            
           

            with open('/home/letchap/tmp/meteo.txt', 'w') as f: 
                f.write("Meteo = " + current_weather.encode('utf8') + "\n")
                f.write("Ville = " + city.encode('utf8') + "\n")
                f.write("Derniere_observation = " + last_observation.encode('utf8') + "\n")
                f.write("Temperature = " + str(current_temp) + " C\n")
                f.write("Ressentie = " + str(feelslike_c) + " C\n")
                f.write("Humidite = " + humidity + "\n")
                f.write("Vent = " + str(wind_kph) + " km/h\n")
                f.write("Dir_vent = " + wind_dir + "\n")
                f.write("Pression = " + str(pressure_mb) + " mb\n")
                f.write("Tend_pres = " + pressure_trend.encode('utf8') + "\n") #Ok
                f.write("Visibilite = " + str(visibility) + " km\n")
                f.write("Indice_UV = " + str(UV) + "\n")
            
            
            
           
            forecast = parsed_json['forecast']['simpleforecast']['forecastday']
            for i in forecast:
                jour           = i['date']['day']        # jour
                mois           = i['date']['month']  # mois
                annee          = i['date']['year']       # 
                jour_sem       = i['date']['weekday']    # 
                period         = i['period']             # 
                tempmax        = i['high']['celsius']    # maximale
                tempmin        = i['low']['celsius']     # minimale
                condition      = i['conditions']         # 
                icon           = i['icon']               # icone en lien avec condition
                skyicon        = i['skyicon']            # couverture nuagueuse
                pop            = i['pop']                # 
                hauteur_precip = i['qpf_allday']['mm']   # 
                hauteur_neige  = i['snow_allday']['cm']  #
                vent           = i['avewind']['kph']     # vitesse moyenne du vent
                vent_dir       = i['avewind']['dir']     # du vent
                tx_humidite    = i['avehumidity']        # 

                
                if period == 1:
                    date = 'jour1'
                elif period == 2:
                    date = 'jour2'
                elif period == 3:
                    date = 'jour3'
                elif period == 4:
                    date = 'jour4'
                
                orage = ['tstorms','chancetstorms','nt_tstorms', 'nt_chancetstorms']
                pluie = ['rain','chancerain','nt_rain', 'nt_chancerain', ]
                neige = ['snow','flurries','chancesnow','chanceflurries','nt_snow','nt_flurries','nt_chancesnow','nt_chanceflurries','sleet', 'nt_sleet','chancesleet','nt_chancesleet']
                # 
                if icon in orage:
                    icone = skyicon+"storm"
                elif icon in pluie:
                    icone = skyicon+"rain"
                elif icon in neige:
                    icone = skyicon+"snow"
                else:
                    icone = icon
                
                
                with open('/home/letchap/tmp/meteo.txt', 'a') as f:
                    f.write(date + "_jour = "  + str(jour) + "\n")
                    f.write(date + "_mois = "  + str(mois) + "\n") 
                    f.write(date + "_annee = "  + str(annee) + "\n")     
                    f.write(date + "_jour_sem = "  + jour_sem.encode('utf8') + "\n") 
                    f.write(date + "_tempmax = "  + str(tempmax) + " C\n")     
                    f.write(date + "_tempmin = "  + str(tempmin) + " C\n")                              
                    f.write(date + "_conditions = " + condition.encode('utf8') + "\n")
                    f.write(date + "_icone = " + icone + "\n")
                    f.write(date + "_pop = "  + str(pop) + "%\n")            
                    f.write(date + "_hauteur_precip = "  + str(hauteur_precip) + " mm\n")            
                    f.write(date + "_hauteur_neige = "  + str(hauteur_neige) + " cm\n")            
                    f.write(date + "_vent = "  + str(vent) + " km/h\n")            
                    f.write(date + "_dir_vent = "  + vent_dir + "\n")             
                    f.write(date + "_tx_himidite = "  + str(tx_humidite) + "%\n")            
    
            ############################################
            #             Le fin du programme          #
            ############################################
            
            time.sleep(120) 
app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()