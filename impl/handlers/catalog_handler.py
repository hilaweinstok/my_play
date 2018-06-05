from tornado.web import RequestHandler, MissingArgumentError
from impl.erorrs import NoSuchFileError, NoSuchIdx
from models.catalog import Catalog


class CatalogHandler(RequestHandler):
    session_maker = None

    def initialize(self, *args, **kwargs):
        self.session_maker = kwargs['session_maker']

    def get(self):
        session = self.session_maker()
        idx = self.get_argument("idx")

        try:
            product = Catalog.GetByIdx(session, idx)
            self.write("data corresponding the idx you enter: {!s}".format(product))
        except NoSuchIdx:
            self.write({'status': 404})
        finally:
            session.close()

    def post(self):
        session = self.session_maker()

        try:
            file_path = self.get_argument("file_path")
            Catalog.SaveData(session, file_path)
            session.commit()

        except MissingArgumentError:
            self.write({'status': 400,
                        'message': 'No such argument'})
        except NoSuchFileError:
            self.write({'status': 404,
                        'message': 'Are you sure the file exists?'})
        finally:
            session.close()

    def delete(self):
        session = self.session_maker()
        idx = self.get_argument("idx")
        try:
            Catalog.DeleteData(session, idx)
            session.commit()
        except NoSuchIdx:
            self.write({'status': 404})
        finally:
            session.close()

# TODO hila- implement the put method