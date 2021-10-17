import time, uuid, logging
from json import dumps, loads
from app.gdb.graph import get_gdb
from app.schemas import UserDetails

gdbservice = get_gdb('prod')



def register_client(appliction):
    '''Create client profile with metadata'''
    now = time.time()
    print(f" ID = {appliction.ref}")
    appliction.signup_ts= now
    appliction.joined= time.ctime(now)
    resp = update_database(appliction)
    return resp


def process_registration(application: UserDetails):
    '''Ensure that the application is unique - based on email & address'''
    if application.ref == "":
        logging.error(f"ID error in {application}")
        return 'error'
    else:
        return application


def update_database(client_profile: UserDetails):
    '''Update Database: with processed and verified client profile.'''
    print(f"Start registration for register_client : {client_profile}")
    query = """
    WITH $json as data
    
    MERGE (client:CLIENT ) ON CREATE
    SET  client.role = data.role, 
    client.id = data.id, 
    client.mobile = data.mobile,
    client.email = data.email, 
    client.username = data.username,
    client.password = data.password, 
    client.signup_ts = data.signup_ts, 
    client.joined = data.joined, 
    client.status = data.status
    """

    print(f"Start graph execution for client {client_profile} \n\n")
    print(f"Start graph execution for client.json {client_profile.json()}")
    client_json = loads(client_profile.json())
    print(f"client_json = {type(client_json)}")
    gdbservice.run(query, json=client_json)
    print(f"Complete graph execution for client {client_profile}")
    return {"success": f"client {client_json['ref']} created successfully"}


def update_client(client_id):
    pass


def get_all_clients():
    print("Start retrieval of ALL CLIENT:")
    query = """
    match (client:CLIENT) return client as clt
    """
    resp = dumps(gdbservice.run(query).data())
    print(f"resp {resp}")
    result = loads(resp)
    print(f"result {result}")
    data = result[0]['clt']
    print(f"data {data}")
    print(f"result of graph execution for job {result}")
    return {"profile":data, "query":query}

def get_client_profile(client_id):
    print(f"Start retrieval of CLIENT: {client_id}")
    query = """
    match (client:CLIENT) where client.id = $client_id return client as clt
    """
    # print(f"Start graph execution for retrieving client {client_id}")
    # print(f"Graph execution with query: {query}")
    resp = dumps(gdbservice.run(query, client_id=client_id).data())
    print(f"resp {resp}")
    result = loads(resp)
    print(f"result {result}")
    data = result[0]['clt']
    print(f"data {data}")
    print(f"Complete graph execution for job {client_id}")
    print(f"result of graph execution for job {result}")
    return {"profile":data, "query":query}


if __name__ == '__main__':
    pass