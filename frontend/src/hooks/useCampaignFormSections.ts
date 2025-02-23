import { useState } from 'react';
import { UseFormGetValues, UseFormSetError, UseFormClearErrors } from 'react-hook-form';
import { CampaignFormData } from '../types/campaign';
import dayjs from 'dayjs';
import { utils } from '@/lib/common-utils';

type ValidationRule = {
  validate: (value: any, getValues?: UseFormGetValues<CampaignFormData>) => boolean;
  message: string;
};

const validationRules: Record<string, ValidationRule> = {
  default: {
    validate: (value) => value !== undefined && value !== null && value !== "" && 
      (!Array.isArray(value) || value.length > 0),
    message: "Field is required"
  },
  numeric: {
    validate: (value) => !isNaN(Number(value)) && Number(value) > 0,
    message: "Must be a positive number"
  },
  file: {
    validate: (value) => (value as FileList)?.length > 0,
    message: "File is required"
  },
  endDate: {
    validate: (value, getValues) => {
      const startDate = getValues?.("start_time");
      if (!startDate || !value) return false;
      return dayjs(value).isAfter(dayjs(startDate));
    },
    message: "End date should be after start date"
  }
};

export const useCampaignFormSections = () => {
  const [activeSection, setActiveSection] = useState(0);
  
  const validateField = (
    field: keyof CampaignFormData,
    value: any,
    getValues: UseFormGetValues<CampaignFormData>
  ): { isValid: boolean; message?: string } => {
    let rule = validationRules.default;
    if (field === "total_budget" || field === "unit_rate") {
      rule = validationRules.numeric;
    } else if (field === "end_time") {
      rule = validationRules.endDate;
    }

    const isValid = rule.validate(value, getValues);
    return {
      isValid,
      message: isValid ? undefined : `${utils.formatProperCase(field.toString().replace(/_/g, " "))} ${rule.message}`
    };
  };

  const nextSection = (
    getValues: UseFormGetValues<CampaignFormData>,
    setError: UseFormSetError<CampaignFormData>,
    clearErrors: UseFormClearErrors<CampaignFormData>,
    mandatoryFields: string[]
  ): boolean => {
    let isValid = true;

    mandatoryFields.forEach((field) => {
      const value = getValues(field as keyof CampaignFormData);
      const validation = validateField(field as keyof CampaignFormData, value, getValues);
      
      if (!validation.isValid) {
        isValid = false;
        setError(field as keyof CampaignFormData, {
          type: "validation",
          message: validation.message
        });
      }
    });

    if (!isValid) {
      return false;
    }

    clearErrors();
    if (activeSection < 7) {
      setActiveSection(activeSection + 1);
      window.scrollTo(0, 0);
      return true;
    }
    return false;
  };

  const prevSection = () => {
    setActiveSection(prev => Math.max(0, prev - 1));
    window.scrollTo(0, 0);
  };

  return { activeSection, nextSection, prevSection };
}; 