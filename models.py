import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import database as _database

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(_database.Base):
    __tablename__ = "users"

    id              = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username           = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    is_active       = _sql.Column(_sql.Boolean, default=True)
    first_name       = _sql.Column(_sql.String)
    last_name        = _sql.Column(_sql.String)
    is_admin        = _sql.Column(_sql.Boolean, default=False)

    addresses       = _orm.relationship("Address", back_populates="owner")

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

class Address(_database.Base):
    __tablename__ = "addresses"
    
    id          = _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_id    = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    city        = _sql.Column(_sql.String)
    country     = _sql.Column(_sql.String)
    street      = _sql.Column(_sql.String)
    postal      = _sql.Column(_sql.String)
    type        = _sql.Column(_sql.String)
    
    owner       = _orm.relationship("User", back_populates="addresses")