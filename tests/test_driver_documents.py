from models import DriverDocument


def test_driver_document_type_allows_qiwa_contract():
    document_type = DriverDocument.__table__.c.document_type.type

    assert "qiwa_contract" in document_type.enums
