from app.models import BandName
from app import db, create_app
from sqlalchemy import exc
from string import capwords

app = create_app()
app.app_context().push()

with open('seed_bands.txt') as seed_bands:
    for band in seed_bands:
        the_band = BandName(band_name=capwords(band))
        try:
            db.session.add(the_band)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()
print('done')
