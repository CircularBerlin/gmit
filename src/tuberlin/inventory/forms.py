from django.forms import ModelForm, ImageField
import uuid
import os

from storages.backends.s3boto3 import S3Boto3Storage

from inventory.models import Objekt, Offer, Comment, Image, Status, OfferStatus, \
    OfferStatusLog, Person, Material


class OfferForm(ModelForm):
    image = ImageField(label='Bild', required=False)

    class Meta:
        model = Offer

        fields = [
            'message',
            'image',
            'import_preferences',
            'email',
            'person_name',
            'phone_number',
            'provider_type',
            'provider_description'
        ]

    def save(self, commit=True):
        self.instance.save()

        file_obj = self.cleaned_data['image']
        if file_obj:
            # organize a path for the file in bucket
            file_directory_within_bucket = 'images/offer/{offer_id}/{guid}'.format(
                offer_id=self.instance.id,
                guid=str(uuid.uuid4())
            )

            # synthesize a full file path; note that we included the filename
            file_path_within_bucket = os.path.join(
                file_directory_within_bucket,
                file_obj.name
            )

            media_storage = S3Boto3Storage()

            # avoid overwriting existing file
            if not media_storage.exists(file_path_within_bucket):
                media_storage.save(file_path_within_bucket, file_obj)

                file_url = "https://{}.s3.amazonaws.com/{}".format(
                    'tuberlin-dev',
                    file_path_within_bucket
                )

                image = Image.objects.create(filename=file_url)
                self.instance.images.add(image)

                if self.instance.thumbnail_image is None:
                    self.instance.thumbnail_image = image

                self.instance.save()

        return super(OfferForm, self).save(commit=commit)


class ObjektForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ObjektForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = 'Haupttitel wird an Restado ??bermittelt.'
        self.fields['unit'].help_text = 'Einheit wird an Restado ??bermittelt.'
        self.fields['width'].help_text = 'Die Breite des Materials in Zentimetern, falls zutreffend. Wird an Restado ??bermittelt.'
        self.fields['width'].help_text = 'Die Breite des Materials in Zentimetern, falls zutreffend. Wird an Restado ??bermittelt.'
        self.fields['height'].help_text = 'Die H??he des Materials in Zentimetern, falls zutreffend. Wird an Restado ??bermittelt.'
        self.fields['depth'].help_text = 'Die Tiefe des Materials in Zentimetern, falls zutreffend. Wird an Restado ??bermittelt.'
        self.fields['mass'].help_text = 'Die Masse des Materials in Kilogramm, falls zutreffend. Wird an Restado ??bermittelt.'
        self.fields['count'].help_text = 'Die Anzahl der Quadratmeter oder Kilogramm des Materials im Lager. Wird an Restado ??bermittelt. F??r undefinierten Betrag leer lassen.'
        self.fields['description'].help_text = 'Beschreibung wird an Restado ??bermittelt.'
        self.fields['treatment_notes'].help_text = 'Behandlungshinweise wird an Restado ??bermittelt.'
        self.fields['condition'].help_text = 'Zustand wird an Restado ??bermittelt.'
        self.fields['price'].help_text = 'Verkaufspreis wird an Restado ??bermittelt.'
        self.fields['eco_cost'].help_text = 'Ecocost wird an Restado ??bermittelt.'
        self.fields['reference_price'].help_text = 'Referenzpreis wird <b>nicht</b> an Restado ??bermittelt.'

    class Meta:
        model = Objekt

        fields = [
            'title',
            'unit',
            'width',
            'height',
            'depth',
            'mass',
            'count',
            'description',
            'treatment_notes',
            'condition',
            'price',
            'eco_cost',
            'reference_price'
        ]


class PersonForm(ModelForm):
    class Meta:
        model = Person

        fields = [
            'email',
            'name',
            'phone_number',
            'notes'
        ]
