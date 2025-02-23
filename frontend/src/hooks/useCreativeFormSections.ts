import { utils } from '@/lib/common-utils';
import { CreativeFormData } from '@/types/creative';
import { useState } from 'react';
import { UseFormClearErrors, UseFormGetValues, UseFormSetError } from 'react-hook-form';

type ValidationRule = {
  validate: (value: any, getValues?: UseFormGetValues<CreativeFormData>) => boolean;
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
    message: "is required"
  },
};

export const useCreativeFormSections = () => {
  const [activeSection, setActiveSection] = useState(0);
  
  const validateField = (
    field: keyof CreativeFormData,
    value: any,
    getValues: UseFormGetValues<CreativeFormData>
  ): { isValid: boolean; message?: string } => {
    let rule = validationRules.default;
    if (["file"].includes(field as string)) {
      rule = validationRules.file;
    }
    const isValid = rule.validate(value, getValues);
    return {
      isValid,
      message: isValid ? undefined : `${utils.formatProperCase(field.toString().replace(/_/g, " "))} ${rule.message}`
    };
  };

  const nextSection = (
    getValues: UseFormGetValues<CreativeFormData>,
    setError: UseFormSetError<CreativeFormData>,
    clearErrors: UseFormClearErrors<CreativeFormData>,
    mandatoryFields: string[]
  ): boolean => {
    let isValid = true;

    mandatoryFields.forEach((field) => {
      const value = getValues(field as keyof CreativeFormData);
      const validation = validateField(field as keyof CreativeFormData, value, getValues);
      
      if (!validation.isValid) {
        isValid = false;
        setError(field as keyof CreativeFormData, {
          type: "validation",
          message: validation.message
        });
      }
    });

    if (!isValid) {
      return false;
    }

    clearErrors();
    if (activeSection < 2) {
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