from pathlib import Path

import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError

from app import CLOUDINARY_CONFIGURED, UPLOAD_FOLDER, get_db_connection


def migrate_images():
    if not CLOUDINARY_CONFIGURED:
        raise RuntimeError("Configurez les trois variables Cloudinary avant le transfert.")

    upload_root = Path(UPLOAD_FOLDER).resolve()
    migrated = 0
    skipped = 0

    with get_db_connection() as connection:
        properties = connection.execute(
            "SELECT id, image FROM properties ORDER BY id"
        ).fetchall()

        for property_item in properties:
            image = property_item["image"]
            if image.startswith(("http://", "https://")):
                skipped += 1
                continue

            source_path = (upload_root / image).resolve()
            if upload_root not in source_path.parents:
                print(f"Annonce {property_item['id']} ignorée : chemin d'image invalide.")
                skipped += 1
                continue
            if not source_path.is_file():
                print(f"Annonce {property_item['id']} ignorée : fichier local introuvable.")
                skipped += 1
                continue

            try:
                with source_path.open("rb") as image_file:
                    result = cloudinary.uploader.upload(
                        image_file,
                        folder="immo-connect/properties",
                        public_id=f"property-{property_item['id']}",
                        overwrite=True,
                        resource_type="image",
                    )
                connection.execute(
                    "UPDATE properties SET image = %s WHERE id = %s",
                    (result["secure_url"], property_item["id"]),
                )
                connection.commit()
                migrated += 1
            except CloudinaryError:
                connection.rollback()
                print(f"Échec de l'envoi de l'image de l'annonce {property_item['id']}.")
                raise

    print(f"Transfert terminé : {migrated} image(s) envoyée(s), {skipped} ignorée(s).")


if __name__ == "__main__":
    migrate_images()