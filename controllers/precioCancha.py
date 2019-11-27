from flask_restful import Resource,reqparse
from models.precioCancha import precioCanchaModel

class precioCanchaController(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "descripcion",
            type=str,
            required=True,
            help="falta la descripcion"
        )
        parser.add_argument(
            "monto",
            type=float,
            required=True,
            help="falta el monto"
        )
        parser.add_argument(
            "disponible",
            type=bool,
            required=True,
            help="falta la disponibilidad"
        )
        parser.add_argument(
            "cancha_id",
            type=int,
            required=True,
            help="falta el id de cancha"
        )
        data = parser.parse_args()
        insercion = precioCanchaModel(data["descripcion"],data["monto"],data["disponible"],data["cancha_id"])
        try:
            insercion.guardar_en_la_bd()
        except:
            return {"message":"hubo un error al agregar un precio a la cancha, intente nuevamente"},500
        return {"message":"se agrego exitosamente el precio a la cancha"+str(insercion.can_id)},201
    def get(self,id):
        resultado = precioCanchaModel.query.filter_by(can_id=id).filter_by(pc_disponibilidad=True).first()
        # print(resultado)
        if resultado:
            return resultado.retornar_json()
        return {"message":"esa cancha aun no tiene precios disponibles"}
    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "estado",
            type=bool,
            required=True,
            help="Falta el estado al que va a ser cambiado el precio de la cancha"
        )
        data = parser.parse_args()
        resultado = precioCanchaModel.query.filter_by(pc_id=id).first()
        try:
            resultado.actualizar_estado(data["estado"])
        except:
            return {
                "message":"hubo un error al actualizar el estado"
            }
        return{"message":"se actualizo el eestado del precio de esa canchita"},200