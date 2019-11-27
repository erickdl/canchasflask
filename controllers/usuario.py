from flask_restful import Resource,reqparse
from models.usuario import UsuarioModel
class usuarioController(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "nombre",
            type=str,
            required=True,
            help="falta el nombre"
        )
        parser.add_argument(
            "apellidos",
            type=str,
            required=True,
            help="falta el apellido"
        )
        parser.add_argument(
            "pass",
            type=str,
            required=True,
            help="falta la contraseña"
        )
        parser.add_argument(
            "tipo",
            type=str,
            required=True,
            help="falta el tipo"
        )
        parser.add_argument(
            "fono",
            type=str,
            required=True,
            help="falta el fono"
        )
        parser.add_argument(
            "correo",
            type=str,
            required=True,
            help="falta el correo"
        )
        data = parser.parse_args()
        consulta = UsuarioModel.query.filter_by(usu_mail=data["correo"]).first()
        if not consulta:
            try:
                UsuarioModel(data["nombre"],data["apellidos"],data["pass"],data["tipo"],data["fono"],data["correo"]).guardar_en_la_bd()
            except:
                return{"messge":"hubo un error al guardar el usuario en la base de datos"},500
            return {"message":"usuario creado con exito"},201
        return {"message":"hay usuario registrado con ese correo"},418
