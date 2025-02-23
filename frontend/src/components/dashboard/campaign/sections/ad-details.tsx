import { Grid, Typography } from '@mui/material';
import { FieldError, UseFormGetValues, UseFormRegister, UseFormSetValue } from 'react-hook-form';
import { CampaignFormData } from '@/types/campaign';
import { FieldErrors } from 'react-hook-form';
import FileUpload from '../../layout/file-upload';
import FormField from '../../layout/form-field';
import { SectionContainer } from '../../layout/section-container';
import { DetailGrid } from '../../layout/section-container';

interface AdDetailsProps {
  register: UseFormRegister<CampaignFormData>;
  getValues: UseFormGetValues<CampaignFormData>;
  setValue: UseFormSetValue<CampaignFormData>;
  errors: FieldErrors<CampaignFormData>;
  campaignType: 'Banner' | 'Video';
}

export const AdDetails = ({
  register,
  getValues,
  setValue,
  errors,
  campaignType
}: AdDetailsProps) => {
  return (
    <SectionContainer title="Ad Details">
      <DetailGrid>
        <Grid item xs={12}>
          <FormField
            type="text"
            placeholder="Landing Page"
            name="landing_page"
            register={register}
            getValues={getValues}
            setValue={setValue}
            error={errors.landing_page as FieldError}
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <FileUpload
            name="tag_tracker"
            register={register}
            setValue={setValue}
            getValue={getValues}
            placeholder="Upload Tag & Tracker"
          />
          {errors.tag_tracker && 
            <Typography sx={{ color: 'red', fontSize: '0.75rem' }}>
              {errors.tag_tracker?.message}
            </Typography>
          }
        </Grid>
        
        {campaignType === 'Banner' ? (
          <Grid item xs={12} md={4}>
            <FileUpload
              name="images"
              register={register}
              setValue={setValue}
              getValue={getValues}
              placeholder="Upload Campaign Image"
            />
            {errors.images && 
              <Typography sx={{ color: 'red', fontSize: '0.75rem' }}>
                {errors.images?.message}
              </Typography>
            }
          </Grid>
        ) : (
          <Grid item xs={12} md={4}>
            <FileUpload
              name="video"
              register={register}
              setValue={setValue}
              getValue={getValues} 
              placeholder="Upload Campaign Video"
            />
            {errors.video && 
              <Typography sx={{ color: 'red', fontSize: '0.75rem' }}>
                {errors.video?.message}
              </Typography>
            }
          </Grid>
        )}
        
        <Grid item xs={12} md={4}>
          <FileUpload
            name="keywords"
            register={register}
            getValue={getValues} 
            setValue={setValue}
            placeholder="Upload Keywords"
          />
          {errors.keywords && 
            <Typography sx={{ color: 'gray', fontSize: '0.75rem' }}>
              {errors.keywords?.message}
            </Typography>
          }
        </Grid>
      </DetailGrid>
    </SectionContainer>
  );
}; 