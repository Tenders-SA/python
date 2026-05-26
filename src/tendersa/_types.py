from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

T = TypeVar("T")


# ── Core Envelope ────────────────────────────────────────────────────────────

@dataclass
class RateLimit:
    limit: int
    remaining: int
    reset: str
    policy: str


@dataclass
class Meta:
    request_id: str
    timestamp: str
    api_version: str
    deprecation: str | None = None
    page: int | None = None
    page_size: int | None = None
    total_count: int | None = None
    total_pages: int | None = None
    has_next: bool | None = None
    has_prev: bool | None = None
    rate_limit: RateLimit | None = None
    query: str | None = None


@dataclass
class ApiResponse(Generic[T]):
    success: bool
    data: T
    meta: Meta


@dataclass
class ApiErrorDetail:
    success: bool = False
    error: str = ""
    code: str = ""
    message: str = ""
    request_id: str = ""
    docs: str = ""
    timestamp: str = ""
    details: dict | None = None


# ── Common ───────────────────────────────────────────────────────────────────

@dataclass
class EstimatedValue:
    min: float | None = None
    max: float | None = None
    median: float | None = None
    confidence: float | None = None
    methodology: str | None = None


# ── Tender ───────────────────────────────────────────────────────────────────

@dataclass
class SourceOrganization:
    name: str


@dataclass
class Subcontractor:
    name: str
    percentage: float | None = None
    bee_level: str | None = None
    black_youth: bool = False
    black_women: bool = False
    black_disabled: bool = False
    black_military: bool = False
    black_rural: bool = False


@dataclass
class Award:
    award_id: str
    currency: str = "ZAR"
    tender_id: str | None = None
    title: str | None = None
    status: str | None = None
    award_date: str | None = None
    amount: float | None = None
    supplier_name: str | None = None
    supplier_id: str | None = None
    enterprise_type: str | None = None
    bee_level: str | None = None
    bee_points: float | None = None
    points: float | None = None
    description: str | None = None
    tender_title: str | None = None
    tender_reference: str | None = None
    tender_category: str | None = None
    tender_province: str | None = None
    subcontractors: list[Subcontractor] | None = None


@dataclass
class Tender:
    tender_id: str
    title: str | None = None
    description: str | None = None
    province: str | None = None
    category: list[dict] = field(default_factory=list)
    estimated_value: EstimatedValue | None = None
    closing_date: str | None = None
    status: str | None = None
    publication_date: str | None = None
    publication_type: str | None = None
    ai_summary: str | None = None
    ai_key_requirements: list[str] | None = None
    ai_confidence: float | None = None
    classification_confidence: float | None = None
    source_organization: SourceOrganization | None = None
    reference_number: str | None = None
    site_url: str | None = None
    municipality: str | None = None
    department: str | None = None
    institution: str | None = None
    data_source: str | None = None


@dataclass
class TenderDocument:
    document_id: str
    file_name: str
    download_url: str
    file_size: int | None = None
    mime_type: str | None = None
    cache_status: str | None = None
    processing_status: str | None = None


@dataclass
class TimelineEvent:
    event: str
    label: str
    date: str
    type: str


@dataclass
class TenderDetail(Tender):
    awards: list[Award] = field(default_factory=list)


@dataclass
class TenderAnalysis:
    id: str
    tender_id: str
    document_id: str | None = None
    submission_guidelines: Any = None
    evaluation_criteria: Any = None
    important_dates: Any = None
    contact_information: Any = None
    technical_specifications: Any = None
    financial_requirements: Any = None
    compliance_requirements: Any = None
    quality_score: float | None = None
    confidence: float | None = None
    ai_model: str | None = None
    ai_extraction_method: str | None = None


@dataclass
class ValueEstimate:
    id: str
    tender_id: str
    estimated_min: float | None = None
    estimated_max: float | None = None
    estimated_median: float | None = None
    confidence_score: float | None = None
    methodology: str | None = None
    data_sources: list[str] | None = None
    factors: Any = None


# ── Company ──────────────────────────────────────────────────────────────────

@dataclass
class Director:
    name: str
    id_number: str | None = None


@dataclass
class CompanyProfile:
    name: str
    total_awards: int = 0
    total_value: float = 0.0
    registration_number: str | None = None
    tax_number: str | None = None
    company_type: str | None = None
    enterprise_type: str | None = None
    bee_level: str | None = None
    cidb_grading: str | None = None
    latest_award_date: str | None = None
    categories: list[str] = field(default_factory=list)
    provinces: list[str] = field(default_factory=list)
    compliance_score: float | None = None
    forensic_risk_score: float | None = None
    director_count: int | None = None
    directors: list[Director] | None = None
    contact_email: str | None = None
    contact_email_confidence: float | None = None
    contact_phone: str | None = None
    website: str | None = None


@dataclass
class CompanyProfileResponse:
    profile: CompanyProfile
    awards: list[Award] = field(default_factory=list)


@dataclass
class CompanySearchResult:
    name: str
    total_awards: int = 0
    total_value: float = 0.0
    registration_number: str | None = None
    enterprise_type: str | None = None
    bee_level: str | None = None
    latest_award_date: str | None = None
    categories: list[str] = field(default_factory=list)
    provinces: list[str] = field(default_factory=list)


# ── Organization ─────────────────────────────────────────────────────────────

@dataclass
class GoogleEnrichment:
    place_id: str
    rating: float | None = None
    map_url: str | None = None
    types: list[str] | None = None


@dataclass
class WikidataEnrichment:
    id: str
    label: str
    description: str


@dataclass
class OrganizationStats:
    total_tenders: int = 0
    total_award_value: float = 0.0
    tender_categories: list[str] | None = None


@dataclass
class OrganizationProfile:
    id: str
    name: str
    organization_type: str | None = None
    legal_name: str | None = None
    registration_number: str | None = None
    bbbee_level: str | None = None
    industry_codes: list[str] | None = None
    provinces_operating: list[str] | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    website: str | None = None
    physical_address: str | None = None
    google: GoogleEnrichment | None = None
    wikidata: WikidataEnrichment | None = None
    gov_directory_url: str | None = None
    salga_municipality_code: str | None = None
    csd_number: str | None = None
    enrichment_sources: list[str] | None = None
    confidence_score: float | None = None
    slug: str | None = None
    stats: OrganizationStats = field(default_factory=OrganizationStats)


@dataclass
class OrganizationTenderSummary:
    tender_id: str
    title: str
    closing_date: str | None = None
    status: str | None = None
    estimated_value: EstimatedValue | None = None


# ── Meta ─────────────────────────────────────────────────────────────────────

@dataclass
class ApiStatus:
    healthy: bool
    version: str
    last_sync: dict


@dataclass
class ProvinceCount:
    name: str
    tender_count: int


@dataclass
class CategoryCount:
    name: str
    count: int


@dataclass
class UsageStats:
    daily: int
    monthly: int
    limit: dict
