import { User } from "./auth";

export interface Location {
    id:number
    country: string;
    state: string;
    city: string;
    tier: string;
    population: number;
}

export interface CommonSelectResponse{
    id: number,
    label?: string,
    value: string
}

export interface Interest{
    id: number,
    subcategory: string
    category: string
}

export interface Images {
    id: number;
    image: string;
    created_at: string;
}

export interface Video {
    id: number;
    video: string;
    created_at: string;
}

export interface FileUpload{
    id: number;
    file: string;
};

export interface Campaign {
    id: number;
    images: Images[];
    keywords: FileUpload[]; 
    name: string;
    age: string[]; 
    day_part: string;
    device: string[]; 
    environment: string[]; 
    exchange: string[];
    target_type: Interest[]; 
    created_at: string; 
    updated_at: string; 
    language: string[];
    carrier: string[]; 
    device_price: string[];  
    proximity_store: FileUpload[]; 
    proximity: FileUpload[];
    weather: FileUpload[]; 
    location: Location[];
    clicks:string;
    pay_rate:string;
    impressions:string;
    objective:string;
    landing_page: string;
    tag_tracker: FileUpload[];
    total_budget: number;
    buy_type: string;
    unit_rate: number;
    ctr:string;
    vtr:string;
    views:string;
    status:string;
    start_time:string;
    end_time:string;
    video: Video[];
    viewability: number;
    brand_safety: number;
    user:User,
    campaign_files:FileUpload[]
}

export interface CampaignFormData  {
    name: string;
    objective: string;
    age: string[];
    device: string[];
    environment: string[];
    location: number[];
    images?: number[];
    keywords?: number[];
    target_type: number[];
    exchange: string[];
    language: string[];
    carrier: string[];
    device_price: string[];
    landing_page?: string;
    tag_tracker?: number[];
    total_budget: number;
    buy_type: string;
    unit_rate: number;  
    viewability: number;
    brand_safety: number;
    video?:number[];
    start_time?: string;
    end_time?: string;
    user?:string
};

export interface CommonImpressionDetails{
    label:string,
    percentage:number
}
export interface ImpressionData{
    totalPopulation: number,
    age?: CommonImpressionDetails[],
    device?: CommonImpressionDetails[],
    environment?: CommonImpressionDetails[],
    carrier?:CommonImpressionDetails[],
}
  