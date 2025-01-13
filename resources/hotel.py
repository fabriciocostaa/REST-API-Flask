from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(cidade = None, estrelas_min = 0,
                           estrelas_max = 5, diaria_min = 0, diaria_max = 10000,
                           limit = 50, offset = 0, **dados):
    if cidade:
        return {
            'estrelas_min' : estrelas_min,
            'estrelas_max' : estrelas_max,
            'diaria_min' : diaria_min,
            'diaria_max' : diaria_max,
            'cidade' : cidade,
            'limit' : limit,
            'offset' : offset }
    return {
        'estrelas_min' : estrelas_min,
        'estrelas_max' : estrelas_max,
        'diaria_min' : diaria_min,
        'diaria_max' : diaria_max,
        'limit' : limit,
        'offset' : offset}

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
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not 'cidade' in parametros:
            # Consulta com 6 parâmetros (sem cidade)
            consulta = "SELECT * FROM hoteis WHERE (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ? and diaria <= ?) LIMIT ? OFFSET ?"
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
            consulta = "SELECT * FROM hoteis WHERE (estrelas >= ? and estrelas <= ?) \
                and (diaria >= ? and diaria <= ?) and cidade = ? LIMIT ? OFFSET ?"
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
                'cidade' : linha[4] })
        
        return {'hoteis' : hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type = str, required = True, help = "This field 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True, help = "This field 'estrelas' cannot be left blank.")
    argumentos.add_argument('diaria', type=float, required=False)
    argumentos.add_argument('cidade', type=str, required=False)

    
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

        try:
            objeto_hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel'}, 500 #Internal Server Error  
        
        return {'message': 'Hotel created successfully.', 'hotel': objeto_hotel.json()}, 201
    
    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        
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