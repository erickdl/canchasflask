from flask_restful import Resource,reqparse
from models.opcionesLocal import opcionesLocalModel
from flask_jwt import jwt_required

class opcionesLocalController(Resource):
    def get(self,nombre):
        resultado = opcionesLocalModel.query.filter_by(ol_desc=nombre).first()
        if resultado:
            print(resultado)
            return resultado.retornar_json()
        return {"message":"no se encuentra una opcion con ese nombre"},404
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("descripcion",
        type=str,
        required=True,
        help="falta ingresar la descripcion")
        data = parser.parse_args()
        ingreso=opcionesLocalModel(data["descripcion"])
        try:
            ingreso.guardar_en_la_bd()
        except:
            return {
                "message":"hubo un error al guardar en la base de datos"
            },500
        return{
            "message":"se guardo exitosamente la opcion ingresada","content":ingreso.retornar_json()
        }

class opcionesLocalTodosController(Resource):
    @jwt_required()
    def get(self):
        resultado = opcionesLocalModel.query.all()
        if resultado:
            resultadoFinal=[]
            for item in resultado:
                resultadoFinal.append(item.retornar_json())
            return resultadoFinal
        return {"message":"no hay opciones que mostrar"},404