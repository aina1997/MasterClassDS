from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast


## INIT THE APP

app = Flask(__name__)
api = Api(app)


## DEFINE CLASS

class Gossos(Resource):
    
    def get(self):
        data = pd.read_csv('./data/gossos.csv')  # read CSV
        data = data.to_dict()  # convert dataframe to dictionary
        return {'data': data}, 200  # return data and 200 OK code
    
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        
        parser.add_argument('id', required=True)  # add args
        parser.add_argument('nom', required=True)
        parser.add_argument('edat', required=True)
        
        args = parser.parse_args()  # parse arguments to dictionary
        
        
        # read our CSV
        data = pd.read_csv('./data/gossos.csv')
        
        if int(args['id']) in list(data['id_gos']):
            return {
                'message': f"'{args['id']}' already exists."
            }, 401
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'id_gos': int(args['id']),
                'nom': args['nom'],
                'edat': int(args['edat'])
            }, index=[0])
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            # save back to CSV
            data.to_csv('./data/gossos.csv', index=False)

            return {'data': data.to_dict()}, 200  # return data with 200 OK
    
    def delete(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('id', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('./data/gossos.csv')
        
        if int(args['id']) in list(data['id_gos']):
            
            data = data.drop(data[data.id_gos == int(args['id'])].index)
            
            # save back to CSV
            data.to_csv('./data/gossos.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{args['id']}' dog not found."
            }, 404
    
class Amos(Resource):
    
    def get(self):
        data = pd.read_csv('./data/amos.csv')  # read CSV
        data = data.to_dict()  # convert dataframe to dictionary
        return {'data': data}, 200  # return data and 200 OK code
    
    def put(self):
        
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('id', required=True)  # add args
        parser.add_argument('id_gos', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('./data/amos.csv')
        
        if int(args['id']) in list(data['id']):
            
            # evaluate strings of lists to lists
            data['Gossos'] = data['Gossos'].apply(
                lambda x: ast.literal_eval(x)
            )
            # select our owner
            owner_data = data[data['id'] == int(args['id'])]

            # update user's locations
            owner_data['Gossos'] = owner_data['Gossos'].values[0] \
                .append(int(args['id_gos']))
            
            # save back to CSV
            data.to_csv('./data/amos.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{args['id']}' user not found."
            }, 404
 
 ## Add Resource

api.add_resource(Gossos, '/gossos')  # '/gossos' és el nostre punt d'entrada per els Gossos
api.add_resource(Amos, '/amos')  # '/amos' és el nostre punt d'entrada per els Amos
    
## Init App
    
if __name__ == '__main__':
    app.run()  # run our Flask app
    