import json
import psycopg2

with open('data.json') as f:
    data = json.loads(f.read()) 

ids = []
names = []
descriptions = []
configs = []
max_frame_sizes = []
port_channel_ids = []

#PORTCHANNEL
for item in data['frinx-uniconfig-topology:configuration']['Cisco-IOS-XE-native:native']['interface']['Port-channel']: 
    id = item['Cisco-IOS-XE-ethernet:service']['instance'][0]['id']
    name = "%s%s" % ('Port-channel', item['name'])    
    config = item

    try: 
        description = item['description']
    except:
        description = None

    try: 
        max_frame_size = item['mtu']  
    except:
       max_frame_size = None

    try: 
        port_channel_id = item['Cisco-IOS-XE-ethernet:channel-group']['number']
    except:
        port_channel_id = None   

    ids.append(id)
    names.append(name)
    descriptions.append(description)
    configs.append(config)
    port_channel_ids.append(port_channel_id)
    max_frame_sizes.append(max_frame_size)    

#TENGIGABITETHERNET    
for item in data['frinx-uniconfig-topology:configuration']['Cisco-IOS-XE-native:native']['interface']['TenGigabitEthernet']:
    try:
        id = item['Cisco-IOS-XE-ethernet:service']['instance'][0]['id']
    except: 
        id = None     
    
    name = "%s%s" % ('TenGigabitEthernet', item['name'])
    config = item

    try:    
        description = item['description']
    except:
        description = None    

    try:    
        max_frame_size = item['mtu']
    except:
        max_frame_size = None    

    try: 
        port_channel_id = item['Cisco-IOS-XE-ethernet:channel-group']['number']
    except:
        port_channel_id = None 

    ids.append(id)
    names.append(name)
    descriptions.append(description)
    configs.append(config)
    port_channel_ids.append(port_channel_id)
    max_frame_sizes.append(max_frame_size)    


#GIGABITETHERNET
for item in data['frinx-uniconfig-topology:configuration']['Cisco-IOS-XE-native:native']['interface']['GigabitEthernet']:
    try:
        id = item['Cisco-IOS-XE-ethernet:service']['instance'][0]['id']
    except: 
        id = None     
    
    name = "%s%s" % ('GigabitEthernet', item['name'])
    config = item   

    try:    
        description = item['description']
    except:
        description = None  

    try:    
        max_frame_size = item['mtu']
    except:
        max_frame_size = None    

    try: 
        port_channel_id = item['Cisco-IOS-XE-ethernet:channel-group']['number']
    except:
        port_channel_id = None 

    ids.append(id)
    names.append(name)
    descriptions.append(description)
    configs.append(config)
    port_channel_ids.append(port_channel_id)
    max_frame_sizes.append(max_frame_size)


#CONNECT TO DB AND INSERT DATA 
conn = psycopg2.connect(user="postgres", password="kaslfjtroe", host="localhost", port="5432", database="frinxdb")
cursor = conn.cursor()

#CHECK IF ID EXIST IN FILE DATA.JSON AND CREATE APPROPRIATE QUERY 
for i in range(len(ids)): 
    if ids[i] == None:
        insert_query = """ INSERT INTO interface (name, description, config, port_channel_id, max_frame_size) VALUES (%s,%s,%s,%s,%s) """
        record_to_insert = (names[i],descriptions[i], json.dumps(configs[i]),port_channel_ids[i],max_frame_sizes[i])
        cursor.execute(insert_query,record_to_insert)
        conn.commit()
    else: 
        insert_query = """ INSERT INTO interface (id,name, description, config, port_channel_id, max_frame_size) VALUES (%s,%s,%s,%s,%s,%s) """
        record_to_insert = (ids[i],names[i],descriptions[i], json.dumps(configs[i]),port_channel_ids[i],max_frame_sizes[i])
        cursor.execute(insert_query,record_to_insert)
        conn.commit()
 



