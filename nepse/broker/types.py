from dataclasses import dataclass
from typing import Any, List


@dataclass
class MembershipTypeMaster:
    id: int
    membership_type: str
    hibernate_lazy_initializer: dict


@dataclass
class Province:
    id: int
    name: str
    description: str
    status: str


@dataclass
class District:
    id: int
    district_name: str
    status: str
    province_id: int


@dataclass
class Municipality:
    id: int
    municipality_name: str
    status: str
    district_id: int


@dataclass
class MemberTmsLinkMapping:
    tms_link: str


@dataclass
class MemberBranchMapping:
    id: int
    branch_name: str
    branch_location: str
    branch_head: Any
    active_status: str
    phone_number: int
    municipality: Municipality
    district: District
    province: Province

    def __post_init__(self) -> None:
        self.district = District(**self.district)
        self.municipality = Municipality(**self.municipality)
        self.province = Province(**self.province)


@dataclass
class BrokerResponse:
    id: int
    active_status: str
    clearing_member_id: int
    member_code: int
    member_name: str
    membership_type_master: MembershipTypeMaster
    authorized_contact_person: int
    authorized_contact_person_number: int
    province_list: List[Province]
    district_list: List[District]
    municipalities: List[Municipality]
    member_tms_link_mapping: MemberTmsLinkMapping
    is_dealer: str
    member_branch_mappings: List[MemberBranchMapping]

    def __post_init__(self) -> None:
        self.member_code = int(self.member_code)

        self.membership_type_master = MembershipTypeMaster(
            **self.membership_type_master
        )
        self.member_tms_link_mapping = MemberTmsLinkMapping(
            **self.member_tms_link_mapping
        )

        self.province_list = [Province(**province) for province in self.province_list]
        self.district_list = [District(**district) for district in self.district_list]
        self.municipalities = [
            Municipality(**municipality) for municipality in self.municipalities
        ]
        self.member_branch_mappings = [
            MemberBranchMapping(**memberBranchMapping)
            for memberBranchMapping in self.member_branch_mappings
        ]
