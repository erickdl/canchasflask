from flask_restful import Resource,reqparse

from models.canchita import CanchitaModel


class CanchitaController(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "tamanio",
            type=str,
            required=True,
            help="falta tamaño"
        )
        parser.add_argument(
            "foto",
            type=str,
            required=True,
            help="falta foto"
        )
        parser.add_argument(
            "local",
            type=int,
            required=True,
            help="falta local"
        )
        parser.add_argument(
            "tipo",
            type=int,
            required=True,
            help="falta tipo"
        )
        data=parser.parse_args()
        canchita = CanchitaModel(data["tamanio"],data["foto"],data["local"],data["tipo"])
        try:
            canchita.guardar_en_la_bd()
        except:
            return{"message":"hubo un error al registrar la canchita,intente nuevamente"},500
        return {"message":"canchita guardada con exito","content":canchita.retornar_json()},200
    def get(self,id):
        resultado = CanchitaModel.query.filter_by(can_id=id).first()
        if resultado:
            return "ok"
        return {"message":"no se encontro el id "+str(id)},404
class CanchitasController(Resource):
    def get(self):
        resultado = CanchitaModel.query.all()
        if resultado:
            arregloResultado=[]
            for item in resultado:
                arregloResultado.append(item.retornar_json())
            print(resultado)
            return arregloResultado
        return "ok"