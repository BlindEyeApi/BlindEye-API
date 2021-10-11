import time, uuid, logging
from json import dumps, loads
from app.gdb.graph import get_gdb
from app.schemas import UserDetails

gdbservice = get_gdb('prod')



def register_client(appliction):
    '''Create client profile with metadata'''
    now = time.time()
    id = str(uuid.uuid4())
    print(f" ID = {id}")
    client = {}
    client["id"] = id
    client["status"]= True
    client["name"]= appliction["name"]
    client["houseNumber"]= appliction["houseNumber"]
    client["location"]= appliction["location"]
    client["password"]= appliction["password"]
    client["signup_ts"]= now
    client["joined"]= time.ctime(now)
    client["JobSheet"]=[]
    resp = process_registration(client)
    if resp != 'error':
        update_database(client)
        return {"status": 200, "msg":f"profile created for {client['id']}" }
    else:
        print(f"application failed - {resp}")
        return {"status": 500, "error":f"ERROR: application failed - {resp}"}
                

def process_registration(application: Client):
    '''Ensure that the application is unique - based on email & address'''
    if application["id"] == "":
        logging.error(f"ID error in {application}")
        return 'error'
    else:
        return application


def update_database(client_profile: Client):
    '''Update Database: with processed and verified client profile.'''
    print(f"Start registration for register_client : {client_profile}")
    query = """
    WITH $json as data
    UNWIND data as q

    MERGE (client:CLIENT {id:q.id}) ON CREATE
    SET client.name = q.name, client.status = q.status, client.houseNumber = q.houseNumber, 
    client.location = q.location, client.JobSheet = q.JobSheet, client.password = q.password, 
    client.signup_ts = q.signup_ts, client.joined = q.joined, client.status = q.status
    """

    print(f"Start graph execution for client {client_profile}")
    gdbservice.run(query,json=client_profile)
    print(f"Complete graph execution for client {client_profile}")
    return {"success":"client created successfully", "query":query}




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