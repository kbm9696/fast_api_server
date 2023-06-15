import logging
from dba.clientsdb import Client, ClientDba
from utils.schemas import CLIENTS_POST, CLIENTS_PATCH, schema_validation
from fastapi.responses import JSONResponse


class ClientsApi:
    def get(self):
        try:
            logging.info('Clients api GET Method')
            resp = {}
            dba = ClientDba()
            data = dba.get()
            resp['description'] = 'All client details'
            resp['details'] = data
            return JSONResponse(content=resp,status_code=200)
        except Exception as e:
            logging.error(f"Got exception in get method: {e}")
            return JSONResponse(content={'Error': str(e)}, status_code=400)

    def post(self, data):
        try:
            logging.info('Clients api POST method')
            client = Client()
            dba = ClientDba()
            if schema_validation(data, CLIENTS_POST):
                return JSONResponse(content={'error': 'error in validation'}, status_code=400)
            client.name = data['name']
            client.email = data['email']
            client.requirement = data['requirement']
            if data.get('age'):
                client.age = data['age']
            if not dba.add(client):
                logging.error("error")
                return {'error': 'error cant able to add new data'}, 400
            logging.info('New Client added successfully')
            return JSONResponse(content={},status_code=201)

        except Exception as e:
            logging.error(f'Got Exception while perform post operation: {e}')
            return JSONResponse(content={'Error':str(e)},status_code=400)


class ClientApi:

    def get(self,cid):
        try:
            logging.info('Client instance api GET Method')
            resp = {}
            dba = ClientDba()
            data = dba.get_by_id(cid)
            if len(data):
                return JSONResponse(content=data,status_code=200)
            else:
                logging.warning(f'Clint Data Not Found for id:{cid}')
                return JSONResponse(content={'message':'data not found'},status_code=404)
        except Exception as e:
            logging.error(f"Got exception in get method: {e}")
            return JSONResponse(content={'Error': str(e)}, status_code=400)

    def patch(self, data, cid):
        try:
            logging.info(f'Client instance update for id:{cid}')
            dba = ClientDba()
            if schema_validation(data, CLIENTS_PATCH):
                logging.error("eroor in validation ")
                return JSONResponse(content={'error': 'error in validation'}, status_code=400)
            res = dba.update(cid,data)
            if res:
                logging.info(f"Data update for client_id:{cid}")
                return JSONResponse(content={},status_code=204)
            else:
                logging.error('Error from database')
                return JSONResponse(content={'Error':'Error in database'}, status_code=400)
        except Exception as e:
            logging.error(f'Got Exception while perform patch operation: {e}')
            return JSONResponse(content={'Error': str(e)}, status_code=400)

    def delete(self, cid):
        try:
            dba = ClientDba()
            dba.delete(cid)
            logging.info(f'deleting client_id:{cid}')
            return JSONResponse(content={}, status_code=204)
        except Exception as e:
            logging.error(f'Got Exception while perform delete operation: {e}')
            return JSONResponse(content={'Error': str(e)}, status_code=400)
