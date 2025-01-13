from flask_restful import Resource, reqparse
from models.usuario import UserModel
import hmac
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blacklist import BLACKLIST
 
atributos = reqparse.RequestParser()
atributos.add_argument('login', type = str, required = True, help = "The field 'login' cannot be left blank")
atributos.add_argument('senha', type = str, required = True, help = "The field 'senha' cannot be left blank")
    
class User(Resource):  
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user is None:
            return {'message': 'User not found.'}, 404
    
        print(user.json())  # Verifique o que está sendo retornado
        return user.json(), 200


    @jwt_required()
    def delete(self, user_id):
        user_encontrado = UserModel.find_user(user_id)
        
        if user_encontrado:
            try:
                user_encontrado.delete()
                return {'message': 'User deleted'}, 200
            except:
                return {'message': 'An error ocurred trying to delete user'}, 500 #Internal Server Error  
        return {'message': 'User not found'}, 404
    
class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()
        if UserModel.find_by_login(dados['login']):
            return {'message' : "The login '{}' already exists" .format(dados['login'])}, 400

        user = UserModel(**dados)
        user.save_user()
        return {"message" : "user created successfully"}, 201 

class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and hmac.compare_digest(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=str(user.user_id))
            return {"message" : token_de_acesso}, 200
        return {"message" : "The username or password is incorret."}, 401 #unauthorized

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        try:
            # Obtenha os dados do token JWT
            jwt_data = get_jwt()

            # Pegue o identificador do token (jti)
            jwt_id = jwt_data.get('jti', None)
            if jwt_id is None:
                return {"message": "Invalid token."}, 400
            
            # Adicione o identificador à blacklist
            BLACKLIST.add(jwt_id)
            return {"message": "Logged out successfully."}, 200
        except:
            return {"message": "An error occurred during logout."}, 500