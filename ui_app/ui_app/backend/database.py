"""Database configuration and models."""

import os
from datetime import date
from decimal import Decimal
from typing import List, Optional

import reflex as rx
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Numeric, Date, Text, create_engine, Computed, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:123456@localhost:5433/postgres"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ProdukDB(Base):
    """Produk database model."""
    __tablename__ = "produk"
    
    id_produk = Column(Integer, primary_key=True, index=True)
    nama_produk = Column(String(100), nullable=False)
    harga_produk = Column(Numeric(12, 2), nullable=False)


class PenjualanDB(Base):
    """Penjualan database model."""
    __tablename__ = "penjualan"
    
    id_penjualan = Column(Integer, primary_key=True, index=True)
    id_produk = Column(Integer, ForeignKey('produk.id_produk'), nullable=False)
    kuantitas = Column(Integer, nullable=False)
    harga_saat_penjualan = Column(Numeric(12, 2), nullable=False)
    total = Column(Numeric(12, 2), Computed('kuantitas * harga_saat_penjualan'), nullable=False)
    catatan = Column(Text)
    tanggal_penjualan = Column(Date, nullable=False)
    
    # Relationship
    produk = relationship("ProdukDB")


class KategoriPengeluaranDB(Base):
    """Kategori Pengeluaran database model."""
    __tablename__ = "kategori_pengeluaran"
    
    id_kategori = Column(Integer, primary_key=True, index=True)
    nama_kategori = Column(String(100), nullable=False)


class BelanjaDB(Base):
    """Belanja database model."""
    __tablename__ = "belanja"
    
    id_belanja = Column(Integer, primary_key=True, index=True)
    deskripsi = Column(Text, nullable=False)
    id_kategori_pengeluaran = Column(Integer, ForeignKey('kategori_pengeluaran.id_kategori'), nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
    metode_pembayaran = Column(String(50), nullable=False)
    bukti_transaksi = Column(String(255))
    catatan = Column(Text)
    tanggal_pengeluaran = Column(Date, nullable=False)
    
    # Relationship
    kategori = relationship("KategoriPengeluaranDB")


# Reflex models for frontend
class Produk(rx.Base):
    """Produk model for frontend."""
    id_produk: int
    nama_produk: str
    harga_produk: float


class KategoriPengeluaran(rx.Base):
    """Kategori Pengeluaran model for frontend."""
    id_kategori: int
    nama_kategori: str


class Penjualan(rx.Base):
    """Penjualan model for frontend."""
    id_penjualan: int
    id_produk: int
    nama_produk: str  # From join with produk table
    kuantitas: int
    harga_saat_penjualan: float
    total: float
    catatan: str
    tanggal_penjualan: str


class Belanja(rx.Base):
    """Belanja model for frontend."""
    id_belanja: int
    deskripsi: str
    id_kategori_pengeluaran: int
    nama_kategori: str  # From join with kategori_pengeluaran table
    total: float
    metode_pembayaran: str
    bukti_transaksi: str
    catatan: str
    tanggal_pengeluaran: str


# Database operations
def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def seed_sample_categories():
    """Add sample categories if none exist."""
    try:
        db = SessionLocal()
        # Check if categories already exist
        existing_count = db.query(KategoriPengeluaranDB).count()
        if existing_count == 0:
            sample_categories = [
                "Food & Beverages",
                "Transportation", 
                "Office Supplies",
                "Marketing",
                "Utilities",
                "Equipment",
                "Other"
            ]
            
            for category_name in sample_categories:
                record = KategoriPengeluaranDB(nama_kategori=category_name)
                db.add(record)
            
            db.commit()
            print(f"Added {len(sample_categories)} sample categories")
        db.close()
    except Exception as e:
        print(f"Error seeding sample categories: {e}")
        if 'db' in locals():
            try:
                db.rollback()
                db.close()
            except:
                pass


def get_produk_data() -> List[Produk]:
    """Get all produk data."""
    try:
        db = SessionLocal()
        records = db.query(ProdukDB).all()
        db.close()
        
        return [
            Produk(
                id_produk=record.id_produk,
                nama_produk=record.nama_produk or "",
                harga_produk=float(record.harga_produk) if record.harga_produk else 0.0,
            )
            for record in records
        ]
    except Exception as e:
        print(f"Error fetching produk data: {e}")
        return []


def get_kategori_pengeluaran_data() -> List[KategoriPengeluaran]:
    """Get all kategori pengeluaran data."""
    try:
        db = SessionLocal()
        records = db.query(KategoriPengeluaranDB).all()
        db.close()
        
        return [
            KategoriPengeluaran(
                id_kategori=record.id_kategori,
                nama_kategori=record.nama_kategori or "",
            )
            for record in records
        ]
    except Exception as e:
        print(f"Error fetching kategori pengeluaran data: {e}")
        return []


def get_penjualan_data() -> List[Penjualan]:
    """Get all penjualan data with product names."""
    try:
        db = SessionLocal()
        # Join penjualan with produk to get product name
        records = db.query(PenjualanDB, ProdukDB.nama_produk).join(
            ProdukDB, PenjualanDB.id_produk == ProdukDB.id_produk
        ).all()
        db.close()
        
        return [
            Penjualan(
                id_penjualan=record[0].id_penjualan,
                id_produk=record[0].id_produk,
                nama_produk=record[1] or "",  # Product name from join
                kuantitas=record[0].kuantitas or 0,
                harga_saat_penjualan=float(record[0].harga_saat_penjualan) if record[0].harga_saat_penjualan else 0.0,
                total=float(record[0].total) if record[0].total else 0.0,
                catatan=record[0].catatan or "",
                tanggal_penjualan=record[0].tanggal_penjualan.strftime("%Y-%m-%d") if record[0].tanggal_penjualan else "",
            )
            for record in records
        ]
    except Exception as e:
        print(f"Error fetching penjualan data: {e}")
        return []


def get_belanja_data() -> List[Belanja]:
    """Get all belanja data with category names."""
    try:
        db = SessionLocal()
        # Join belanja with kategori_pengeluaran to get category name
        records = db.query(BelanjaDB, KategoriPengeluaranDB.nama_kategori).join(
            KategoriPengeluaranDB, BelanjaDB.id_kategori_pengeluaran == KategoriPengeluaranDB.id_kategori
        ).all()
        db.close()
        
        return [
            Belanja(
                id_belanja=record[0].id_belanja,
                deskripsi=record[0].deskripsi or "",
                id_kategori_pengeluaran=record[0].id_kategori_pengeluaran or 0,
                nama_kategori=record[1] or "",  # Category name from join
                total=float(record[0].total) if record[0].total else 0.0,
                metode_pembayaran=record[0].metode_pembayaran or "",
                bukti_transaksi=record[0].bukti_transaksi or "",
                catatan=record[0].catatan or "",
                tanggal_pengeluaran=record[0].tanggal_pengeluaran.strftime("%Y-%m-%d") if record[0].tanggal_pengeluaran else "",
            )
            for record in records
        ]
    except Exception as e:
        print(f"Error fetching belanja data: {e}")
        return []


def insert_produk(data: dict) -> bool:
    """Insert new produk record."""
    try:
        db = SessionLocal()
        
        nama_produk_val = data.get("nama_produk", "").strip()
        try:
            harga_produk_val = Decimal(str(data["harga_produk"])) if data.get("harga_produk") and str(data["harga_produk"]).strip() else Decimal("0")
        except (ValueError, TypeError):
            harga_produk_val = Decimal("0")
        
        if not nama_produk_val:
            print("Product name is required")
            db.close()
            return False
        
        record = ProdukDB(
            nama_produk=nama_produk_val,
            harga_produk=harga_produk_val,
        )
        db.add(record)
        db.commit()
        
        # Get the ID of the inserted product
        new_id = record.id_produk
        db.close()
        print(f"Product added successfully with ID: {new_id}")
        return new_id
    except Exception as e:
        print(f"Error inserting produk data: {e}")
        import traceback
        traceback.print_exc()
        if 'db' in locals():
            try:
                db.rollback()
                db.close()
            except:
                pass
        return False


def insert_kategori_pengeluaran(data: dict) -> bool:
    """Insert new kategori pengeluaran record."""
    try:
        db = SessionLocal()
        
        nama_kategori_val = data.get("nama_kategori", "").strip()
        
        # Validate required fields
        if not nama_kategori_val:
            print("Missing required field: nama_kategori")
            db.close()
            return False
        
        record = KategoriPengeluaranDB(
            nama_kategori=nama_kategori_val,
        )
        db.add(record)
        db.commit()
        
        # Get the ID of the inserted category
        new_id = record.id_kategori
        db.close()
        print(f"Category added successfully with ID: {new_id}")
        return new_id
    except Exception as e:
        print(f"Error inserting kategori pengeluaran data: {e}")
        import traceback
        traceback.print_exc()
        if 'db' in locals():
            try:
                db.rollback()
                db.close()
            except:
                pass
        return False


def insert_penjualan(data: dict) -> bool:
    """Insert new penjualan record."""
    try:
        db = SessionLocal()
        
        # Debug: Print the incoming data
        print(f"Inserting penjualan data: {data}")
        
        # Validate and convert data
        tanggal_val = None
        if data.get("tanggal_penjualan") and data["tanggal_penjualan"].strip():
            try:
                tanggal_val = date.fromisoformat(data["tanggal_penjualan"])
            except ValueError:
                print(f"Invalid date format: {data['tanggal_penjualan']}")
                tanggal_val = date.today()
        else:
            tanggal_val = date.today()
            
        # Handle numeric fields with validation
        try:
            id_produk_val = int(data["id_produk"]) if data.get("id_produk") else 0
        except (ValueError, TypeError):
            id_produk_val = 0
            
        try:
            kuantitas_val = int(data["kuantitas"]) if data.get("kuantitas") and str(data["kuantitas"]).strip() else 0
        except (ValueError, TypeError):
            kuantitas_val = 0
            
        try:
            harga_saat_penjualan_val = Decimal(str(data["harga_saat_penjualan"])) if data.get("harga_saat_penjualan") and str(data["harga_saat_penjualan"]).strip() else Decimal("0")
        except (ValueError, TypeError):
            harga_saat_penjualan_val = Decimal("0")
            
        catatan_val = data.get("catatan", "").strip()
        
        # Validate required fields
        if not id_produk_val or kuantitas_val <= 0:
            print("Missing required fields: product and quantity")
            db.close()
            return False
        
        record = PenjualanDB(
            id_produk=id_produk_val,
            kuantitas=kuantitas_val,
            harga_saat_penjualan=harga_saat_penjualan_val,
            catatan=catatan_val,
            tanggal_penjualan=tanggal_val,
        )
        db.add(record)
        db.commit()
        db.close()
        print("Penjualan data inserted successfully")
        return True
    except Exception as e:
        print(f"Error inserting penjualan data: {e}")
        import traceback
        traceback.print_exc()
        if 'db' in locals():
            try:
                db.rollback()
                db.close()
            except:
                pass
        return False


def insert_belanja(data: dict) -> bool:
    """Insert new belanja record."""
    try:
        db = SessionLocal()
        
        # Debug: Print the incoming data
        print(f"Inserting belanja data: {data}")
        
        # Validate and convert data
        tanggal_val = None
        if data.get("tanggal_pengeluaran") and data["tanggal_pengeluaran"].strip():
            try:
                tanggal_val = date.fromisoformat(data["tanggal_pengeluaran"])
            except ValueError:
                print(f"Invalid date format: {data['tanggal_pengeluaran']}")
                tanggal_val = date.today()
        else:
            tanggal_val = date.today()
            
        deskripsi_val = data.get("deskripsi", "").strip()
        
        try:
            id_kategori_pengeluaran_val = int(data["id_kategori_pengeluaran"]) if data.get("id_kategori_pengeluaran") else 0
        except (ValueError, TypeError):
            id_kategori_pengeluaran_val = 0
            
        try:
            total_val = Decimal(str(data["total"])) if data.get("total") and str(data["total"]).strip() else Decimal("0")
        except (ValueError, TypeError):
            total_val = Decimal("0")
            
        metode_pembayaran_val = data.get("metode_pembayaran", "").strip()
        bukti_transaksi_val = data.get("bukti_transaksi", "").strip()
        catatan_val = data.get("catatan", "").strip()
        
        # Validate required fields
        if not deskripsi_val or not metode_pembayaran_val:
            print("Missing required fields")
            db.close()
            return False
        
        record = BelanjaDB(
            deskripsi=deskripsi_val,
            id_kategori_pengeluaran=id_kategori_pengeluaran_val,
            total=total_val,
            metode_pembayaran=metode_pembayaran_val,
            bukti_transaksi=bukti_transaksi_val,
            catatan=catatan_val,
            tanggal_pengeluaran=tanggal_val,
        )
        db.add(record)
        db.commit()
        db.close()
        print("Belanja data inserted successfully")
        return True
    except Exception as e:
        print(f"Error inserting belanja data: {e}")
        import traceback
        traceback.print_exc()
        if 'db' in locals():
            try:
                db.rollback()
                db.close()
            except:
                pass
        return False
