from sqla import sqla
from sqlalchemy.orm import validates
class Card(sqla.Model):
    __tablename__ = "cards"
    id              = sqla.Column(sqla.Integer(), primary_key=True)
    question        = sqla.Column(sqla.Text(), nullable=False)
    answer        = sqla.Column(sqla.Text(), nullable=False)

    @validates
    def validate_not_empty(self, key, value):
        if not value:
            raise ValueError(f'{key.capitalize()} is required.')
        return value