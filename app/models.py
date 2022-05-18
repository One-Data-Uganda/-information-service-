# coding: utf-8
from sqlalchemy import CHAR, Column, Date, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from app.db.base_class import Base

metadata = Base.metadata


class Region(Base, SerializerMixin):
    __tablename__ = "region"

    id = Column(Text, primary_key=True)

    subregions = relationship("SubRegion")


class SubRegion(Base, SerializerMixin):
    __tablename__ = "sub_region"

    id = Column(Text, primary_key=True)
    subregion_id = Column(
        ForeignKey("region.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    countries = relationship("Country")


class Country(Base, SerializerMixin):
    __tablename__ = "country"

    id = Column(CHAR(2), primary_key=True)
    subregion_id = Column(
        ForeignKey("sub_region.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    calling_code = Column(Integer)
    name = Column(Text)
    other_names = Column(Text)
    motto = Column(Text)
    date_of_independence = Column(Date)
    introduction = Column(Text)
    location = Column(Text)
    neighbours = Column(Text)
    capital_city = Column(Text)
    population = Column(Float(53))
    languages = Column(Text)
    facts_and_figures = Column(Text)
    classification = Column(Text)
    life_expectancy = Column(Float)
    median_age = Column(Float)
    average_children = Column(Float)
    income_group = Column(Text)
    employment_rate = Column(Float)
    unemployment_rate = Column(Float)
    contribution_men = Column(Float)
    contribution_women = Column(Float)
    gdp_2019 = Column(Float(53))
    gdp_per_capita = Column(Float)
    growth_of_gdp = Column(Float)
    inflation = Column(Float)
    investment = Column(Float)
    total_debt = Column(Float)
    gnp_per_capita = Column(Float)
    corruption_rank = Column(Float)
    credit_rank = Column(Float)
    business_score = Column(Float)
    key_sectors_growth = Column(Text)
    key_issues = Column(Text)

    contacts = relationship("CountryContact")
    documents = relationship("CountryDocument")
    sectors = relationship("CountrySector")


class CountryContact(Base, SerializerMixin):
    __tablename__ = "country_contact"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(
        ForeignKey("country.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    updated_at = Column(DateTime)
    govt_contact = Column(Text)
    economic_contact = Column(Text)
    parliament_contact = Column(Text)
    judiciary_contact = Column(Text)


class CountryDocument(Base, SerializerMixin):
    __tablename__ = "country_document"

    id = Column(UUID(as_uuid=True), primary_key=True)
    country_id = Column(
        ForeignKey("country.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    document_type = Column(Text)
    name = Column(Text)
    filesize = Column(Integer)
    filetype = Column(Text)


class CountrySector(Base, SerializerMixin):
    __tablename__ = "country_sector"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(
        ForeignKey("country.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    sector_id = Column(ForeignKey("sector.id", ondelete="CASCADE", onupdate="CASCADE"))
    contribution_to_gdp = Column(Float)
    growth_rate = Column(Float)

    sector = relationship("Sector")


class SectorIndustry(Base, SerializerMixin):
    __tablename__ = "sector_industry"

    id = Column(Text, primary_key=True)
    name = Column(Text)

    divisions = relationship("SectorDivision")


class SectorDivision(Base, SerializerMixin):
    __tablename__ = "sector_division"

    id = Column(Text, primary_key=True)
    sector_industry_id = Column(
        ForeignKey("sector_industry.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    name = Column(Text)

    groups = relationship("SectorGroup")


class SectorGroup(Base, SerializerMixin):
    __tablename__ = "sector_group"

    id = Column(Text, primary_key=True)
    sector_division_id = Column(
        ForeignKey("sector_division.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    name = Column(Text)

    sectors = relationship("Sector")


class Sector(Base, SerializerMixin):
    __tablename__ = "sector"

    id = Column(Text, primary_key=True)
    sector_group_id = Column(
        ForeignKey("sector_group.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    name = Column(Text)
