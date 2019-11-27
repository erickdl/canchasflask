from flask_restful import Resource,reqparse
from models.reserva import reservaModel
from flask_jwt import jwt_required

class ReservaController(Resource):
    # @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "fecha_inicio",
            type=str,
            required=True,
            help="falta el fecha inicio"
        )
        parser.add_argument(
            "fecha_fin",
            type=str,
            required=True,
            help="falta la fecha fin"
        )
        parser.add_argument(
            "monto",
            type=float,
            required=True,
            help="falta el monto"
        )
        parser.add_argument(
            "adelanto",
            type=float,
            required=True,
            help="falta el adelanto"
        )
        parser.add_argument(
            "id_usu",
            type=int,
            required=True,
            help="falta el id de usuario"
        )
        parser.add_argument(
            "precio_cancha",
            type=int,
            required=True,
            help="falta el precio de la cancha"
        )
        data = parser.parse_args()
        validar = reservaModel.query.filter_by(pc_id=data["precio_cancha"]).all()
        from datetime import datetime
        fechaintroducidainicio = datetime.strptime(data["fecha_inicio"],"%Y-%m-%d %H:%M")
        fechaintroducidafin = datetime.strptime(data["fecha_fin"],"%Y-%m-%d %H:%M")
        print(fechaintroducidainicio)
        for sentencia in validar:
            fechaencontradainicio = sentencia.res_fechin
            fechaencontradafin = sentencia.res_fechfin
            if (fechaintroducidainicio >= fechaencontradainicio and fechaintroducidainicio < fechaencontradafin) or (fechaintroducidafin > fechaencontradainicio and fechaintroducidafin <= fechaencontradafin) or (fechaintroducidainicio == fechaencontradainicio and fechaintroducidafin == fechaencontradafin) or (fechaintroducidainicio < fechaencontradainicio and fechaintroducidafin > fechaencontradafin):
                return {"message":"ya hay una reserva en ese horario"},403
        insercion = reservaModel(data["fecha_inicio"],data["fecha_fin"],data["monto"],data["adelanto"],data["id_usu"],data["precio_cancha"])
        try:
            insercion.guardar_en_la_bd()
        except:
            return {
                'message':'Hubo un error al guardar la reserva, intentelo nuevamente'},500
        return {
            'message':'Reservada creada satisfactoriamente',
            'content':insercion.res_id
            },201
        