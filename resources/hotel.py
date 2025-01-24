from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required
from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade
import sqlite3

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str, location='args')
path_params.add_argument('estrelas_min', type=float, location='args')
path_params.add_argument('estrelas_max', type=float, location='args')
path_params.add_argument('diaria_min', type=float, location='args')
path_params.add_argument('diaria_max', type=float, location='args')
path_params.add_argument('limit', type=int, location='args')
path_params.add_argument('offset', type=int, location='args')

class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('instance/banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not 'cidade' in parametros:
            # Consulta com 6 parâmetros (sem cidade)
            consulta = consulta_sem_cidade
            tupla = (
                parametros['estrelas_min'],
                parametros['estrelas_max'],
                parametros['diaria_min'],
                parametros['diaria_max'],
                parametros['limit'],
                parametros['offset']
            )
        else:
            # Consulta com 7 parâmetros (incluindo cidade)
            consulta = consulta_com_cidade
            tupla = (
                parametros['estrelas_min'],
                parametros['estrelas_max'],
                parametros['diaria_min'],
                parametros['diaria_max'],
                parametros['cidade'],
                parametros['limit'],
                parametros['offset']
            )

        resultado = cursor.execute(consulta, tupla)

        hoteis = []
        for linha in resultado: 
            hoteis.append ({
                'hotel_id' : linha [0], #acessando coluna [0]
                'nome' : linha[1], #coluna [1]
                'estrelas' : linha[2],
                'diaria': linha[3],
                'cidade' : linha[4],
                'site_id': linha[5] })
        
        return {"hoteis": hoteis} 
    
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type = str, required = True, help = "This field 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True, help = "This field 'estrelas' cannot be left blank.")
    argumentos.add_argument('diaria', type=float, required=False)
    argumentos.add_argument('cidade', type=str, required=False)
    argumentos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site")

    
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel == None:
            return {'message': 'Hotel not found.'}, 404 
        else:
            return hotel.json(), 200

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel_id  '{}' already exist!" .format(hotel_id)}, 400 #bad request
        
        dados = Hotel.argumentos.parse_args()
        objeto_hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados['site_id']):
            return {'message' : 'the hotel must be associated to a valid site id'}, 400
        try:
            objeto_hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500 #Internal Server Error  
        
        return {'message': 'Hotel created successfully.', 'hotel': objeto_hotel.json()}, 201
    
    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        
        if not SiteModel.find_by_id(dados['site_id']):
            return {'message' : 'the hotel must be associated to a valid site id'}, 400
        
        if hotel_encontrado:
            hotel_encontrado.update(**dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {'message': 'An internal error ocurred trying to save hotel'}, 500 #Internal Server Error  
            return hotel_encontrado.json(), 200 #OK

        objeto_hotel = HotelModel(hotel_id, **dados)
        
        try:
            objeto_hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500 #Internal Server Error  
        
        return objeto_hotel.json(), 201 #created


    @jwt_required()
    def delete(self, hotel_id):
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        
        if hotel_encontrado:
            try:
                hotel_encontrado.delete()
            except:
                return {'message': 'An error ocurred trying to delete hotel'}, 500 #Internal Server Error  
            return {'message': 'Hotel deleted'}, 200
        return {'message': 'hotel not found'}, 404