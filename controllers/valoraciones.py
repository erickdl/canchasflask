from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.valoraciones import valoracionesModel
from models.local import LocalModel
class valoracionController():
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "comentario",
            type=str,
            required=True,
            help="falta el comentario"
        )
        parser.add_argument(
            "estrellas",
            type=str,
            required=True,
            help="falta la cantidad de estrellas"
        )
        parser.add_argument(
            "id_reserva",
            type=str,
            required=True,
            help="falta el id de la reserva"
        )
        data = parser.parse_args()
        valoracion=valoracionesModel(data["comentario"],data["estrellas"],data["id_reserva"])
        try:
            valoracion.guardar_en_la_bd()
        except:
            return {
                "message":"hubo un error al ingresar tu comentario, intentalo nuevamente"
            },500
        return {
            "message":"se agrego exitosamente el comentario","content":valoracion.val_id
        }
class valoracionesController(Resource):
    def get(self,id):
        sentencia = LocalModel.query.filter_by(loc_id=id).first()
        resultado=[]
        promedio=0
        for cancha in sentencia.canchitas:
            # print(cancha)
            for preciocancha in cancha.precio:
                # print(preciocancha)
                for reserva in preciocancha.reserva:
                    # print(reserva)
                    for valoracion in reserva.val:
                        promedio += valoracion.val_estrellas
                        resultado.append({
                            "comentario":valoracion.val_comentario,
                            "estrellas":valoracion.val_estrellas
                        })
        return {
            "comentario":resultado,
            "promedio":promedio/len(resultado)
        }
                        
       