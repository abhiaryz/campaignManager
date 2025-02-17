"use client"
import { campaignClient } from '@/lib/campaign-client';
import { utils } from '@/lib/common-utils';
import { paths } from '@/paths';
import { CampaignFormData, CommonSelectResponse, ImpressionData, Interest, Location } from '@/types/campaign';
import { CampaignFormSchema } from '@/types/schema';
import { zodResolver } from '@hookform/resolvers/zod';
import { Alert, Box, Button, CircularProgress, Grid, SelectChangeEvent, TextField, Typography } from '@mui/material';
import dayjs from 'dayjs';
import { useRouter } from 'next/navigation';
import * as React from 'react';
import { useForm } from 'react-hook-form';
import FileUpload from '../layout/file-upload';
import FormField from '../layout/form-field';
import { ProgressIndicator } from '../layout/progress-indicator';
import { DetailGrid, SectionContainer } from '../layout/section-container';
import TargetType from '../layout/target-type';
import { CampaignReview } from './campaign-review';
import { CampaignTypeSelector } from './campaign-select';
import { ImpressionComponent } from './impression-panel';
import { useAuth } from '@/hooks/use-auth';
import { User } from '@/types/auth';

export default function CreateCampaign(): React.JSX.Element {

    const router = useRouter();
    const {auth} = useAuth();
    const [dataSources, setDataSources] = React.useState({
      ages: [],
      devices: [],
      environment: [],
      location: [],
      exchange: [],
      language: [],
      carrier: [],
      device_price: [],
      interest_category: [],
      interest: [],
      selectedInterest: [],
      buy_type: [],
      brand_safety: [],
      viewability: [],
      users: [],
    } as Record<string, CommonSelectResponse[] | Location[] | Interest[] |User[]>);
    const [impressionData,setImpressionData] = React.useState<ImpressionData>();
    const [totalPopulation,setTotalPopulation] = React.useState<number>(0);
    const [isPending, setIsPending] = React.useState<boolean>(false);
    const [isCampaignCreated,setIsCampaignCreated] = React.useState<boolean>(false);
    const [targetPopulation, setTargetPopulation] = React.useState<number>(0);
    const [activeSection, setActiveSection] = React.useState<number>(0); 
    const [campaignType, setCampaignType] = React.useState<'Banner' | 'Video'>('Banner');
    const [targetType, setTargetType] = React.useState<string>('');
    const [isEditable,setIsEditable] = React.useState<boolean>(false);
    const [campaignId,setCampaignId] = React.useState<number>(-1);
    const [filteredBuyTypeList,setFilteredBuyTypeList] = React.useState<CommonSelectResponse[]>([]);
    const mandatoryFieldsBySection: Record<number, string[]> = {
      0: ["objective"], 
      // 1: [],
      // 2: [],
      // 3: [],
      // 4: []
      1: ["name","start_time","end_time"], 
      2: ["location", "age", "exchange", "language", "viewability", "brand_safety","device", "environment", "carrier", "device_price"],
      3: ["target_type"],
      4: campaignType === "Banner" ? ["tag_tracker","total_budget", "buy_type", "unit_rate"] : ["video","tag_tracker","total_budget", "buy_type", "unit_rate"],
    };
    
    const {
      register,
      setValue,
      setError,
      clearErrors,
      handleSubmit,
      getValues,
      formState: { errors },
    } = useForm<CampaignFormData>({ resolver: zodResolver(CampaignFormSchema) });
  
    const fetchData = async () => {
      try {
        const [ageRes, deviceRes, envRes, locRes,exchangeRes,langRes,
          carrierRes,devicePriceRes, categoryInterestRes,interestRes, impressionRes,buyTypeRes,
          viewabilityRes,brandSafetyRes,userRes] = await Promise.all([
          campaignClient.getAge(),
          campaignClient.getDevice(),
          campaignClient.getEnv(),
          campaignClient.getLocations(),
          campaignClient.getExchange(),
          campaignClient.getLanguage(),
          campaignClient.getCarrier(),
          campaignClient.getDevicePrice(),
          campaignClient.getDistinctInterest(),
          campaignClient.getInterest(""),
          campaignClient.getImpressionData(),
          campaignClient.getBuyType(),
          campaignClient.getViewability(),
          campaignClient.getBrandSafety(),
          campaignClient.getUsers(auth?.usertype === 'admin')
        ]);
        setDataSources({
          ages: ageRes,
          devices: deviceRes,
          environment: envRes,
          location: locRes,
          exchange: exchangeRes,
          language: langRes,
          carrier: carrierRes,
          device_price: devicePriceRes,
          interest_category: categoryInterestRes,
          interest: interestRes,
          selectedInterest: [],
          buy_type:buyTypeRes,
          viewability:viewabilityRes,
          brand_safety:brandSafetyRes,
          users:userRes
        });
        setImpressionData(impressionRes)
        setTotalPopulation(impressionRes.totalPopulation)
      } catch (error) {
        setError('root', { type: 'server', message: "Failed to load campaign data. Error: " + error });
      }finally{
        setIsPending(false)
      }
    };

    const onSubmit = async (data: CampaignFormData) => {
      clearErrors();
      if(!data) 
        return;

      setIsPending(true);
      try {
        const result = await campaignClient.createUpdateCampaign(data,isEditable,campaignId);
        if (result) {
          setIsCampaignCreated(true);
          router.push(paths.dashboard.overview);
        }
      } catch (error:any) {
        setError('root', { type: 'server', message: error.message});
      } finally {
        setIsPending(false);
      }
    };
  
    const handleSelectChange = async (event: SelectChangeEvent<unknown>,name: string) => {  
      if(name.startsWith('target_type')){
        const selectedValue: number[] = event.target.value as number[];
        const selectedTargetType = getValues("target_type")? Array.from(
          new Set([...selectedValue, ...getValues("target_type") as Number[]])
        ) as number[]:selectedValue;
        setValue("target_type",selectedTargetType)
        setTargetType(utils.formatTargetIdToSubCategory(selectedTargetType,dataSources.interest as Interest[]));
      }
      
      if(["location","age"].includes(name) && impressionData && dataSources){
        setTargetPopulation(utils.calculateTargetPopulation(name,dataSources.location as  Location[]
          ,getValues,impressionData,event))
      }
    };

    const nextSection = () => {
      const mandatoryFields = mandatoryFieldsBySection[activeSection];
    
      const isSectionValid = mandatoryFields.every((field) => {
        const value = getValues(field as  keyof CampaignFormData);
        const isValidField = value !== undefined && value !== null && value !== "" && (!Array.isArray(value) || value.length > 0);;
        if(field === "total_budget" || field === "unit_rate") {
          return isValidField && !isNaN(Number(value)) && Number(value) > 0;
        }
        
        if(field === "images" || field === "video" || field === "tag_tracker") {
          return isValidField &&  (value as unknown as FileList).length > 0;
        }
        
        if(field === "end_time"){
          const startDate = getValues("start_time") as unknown as number;
          return isValidField && dayjs(value as number).isAfter(dayjs(startDate));
        }
        return isValidField;
      });
          
      if (!isSectionValid) {
        mandatoryFields.find((field) => {
          const value = getValues(field as  keyof CampaignFormData);
          let isFieldMissing =  value === undefined || value === null || value === "" || (Array.isArray(value) && value.length === 0) 
          let startDateError = false;
          if(field === "total_budget" || field === "unit_rate"){
             isFieldMissing = isFieldMissing || isNaN(Number(value)) || Number(value) <= 0;
          }else if(field === "images" || field === "video" || field === "tag_tracker"){
            isFieldMissing= isFieldMissing || (value as unknown as FileList).length === 0;
          }else if(field === "end_time"){
            const startDate = getValues("start_time") as unknown as number;
            startDateError = isFieldMissing || !dayjs(value as number).isAfter(dayjs(startDate));
          }
          
          if (isFieldMissing) {
            const capitalizeFirstLetter = field.charAt(0).toUpperCase() + field.slice(1);
            setError(field as  keyof CampaignFormData, {type: "required",message: `${capitalizeFirstLetter.replace("_"," ")} field is required`});
          }

          if(startDateError){
            setError(field as  keyof CampaignFormData, {type: "invalid",message: "End date should be after start date"});
          }
        });
        return;
      } 

      clearErrors();
      if (activeSection < 7) {
        setActiveSection(activeSection + 1);
      }
    };

    const prevSection = () => {
      if (activeSection > 0) {
          setActiveSection(activeSection - 1);
      }
    };
  
    const setFormDataOnEdit = ()=>{
      const storedCampaign = sessionStorage.getItem("campaign");
      const storedCampaignId = sessionStorage.getItem("id") ? Number(sessionStorage.getItem("id")):-1;
      if (storedCampaign && storedCampaignId !== -1) {
        setIsEditable(true);
        setCampaignId(storedCampaignId);
        const parsedCampaign = JSON.parse(storedCampaign);
        sessionStorage.clear()
        Object.keys(parsedCampaign).forEach((key) => {
          if(key === "objective"){
            setCampaignType(parsedCampaign[key])
          }
          setValue(key as keyof CampaignFormData, parsedCampaign[key]);
        });  
      }
    }
    
    React.useEffect(() => {
      fetchData();
      setFormDataOnEdit();
      
      if(getValues("target_type")){
        setTargetType(utils.formatTargetIdToSubCategory(getValues("target_type"),dataSources.interest as Interest[]));
      }

      if(!getValues("objective")){
        setValue('objective', 'Banner');
      }

      if(impressionData && dataSources){
        setTargetPopulation(utils.calculateTargetPopulation("ages",dataSources.location as  Location[]
          ,getValues,impressionData,undefined))
      }    

      if (dataSources && dataSources.buy_type.length > 0) {
        const filteredBuyTypes = (dataSources.buy_type as CommonSelectResponse[]).filter((buyType) => {
          if (campaignType === 'Banner') {
            return buyType.value !== 'CPV';
          } else if (campaignType === 'Video') {
            return buyType.value !== 'CPC';
          }
          return true;
        });
        setFilteredBuyTypeList(filteredBuyTypes);
      }
    }, [campaignType,targetPopulation,targetType,dataSources]);
  
    return (
      <Box
        sx={{
          display: "flex",
          flexDirection: {
            xs: "column",
            sm: "column",
            md: "row",
          },
          justifyContent: "space-between",
          alignItems: "flex-start",
          gap: { xs: 2, sm: 3, md: 4 },
          p: { xs: 1, sm: 2, md: 3 },
          
        }}
      >
        <Box sx={{ flex: { xs: "1", md: "2" , lg:"3"}, overflow: "hidden" }}>
          <form onSubmit={handleSubmit(onSubmit)}>
            <Box sx={{ display: "flex", 
                flexDirection: "column",
                gap: 3 ,
                border: 1,
                padding:2 ,
                borderColor: "grey.300",
            }}>

              <ProgressIndicator activeSection={activeSection} totalSections={6} />

              {activeSection === 0 && (
                 <SectionContainer title="Campaign Type">
                    <CampaignTypeSelector 
                      campaignType={campaignType} 
                      setCampaignType={setCampaignType} 
                      setValue={setValue} 
                      isEditable ={isEditable} />
                  </SectionContainer>
               )}

              {activeSection === 1 && (
                <SectionContainer title="Campaign Details">
                    <DetailGrid>
                      {/* Name Field - Full Width */}
                      <Grid item xs={12}>
                        <FormField
                          type="text"
                          placeholder="Name"
                          name="name"
                          getValues={getValues}
                          setValue={setValue}
                          register={register}
                          error={errors.name}
                        />
                      </Grid>

                    {auth?.usertype === 'admin' && (
                        <Grid item xs={12}>
                          <FormField
                            type="select"
                            placeholder="User"
                            name='user'
                            register={register}
                            getValues={getValues}
                            setValue={setValue}
                            multiple = {false}
                            onChange={handleSelectChange}
                            error={Array.isArray(errors.user) ? errors.user[0] : errors.user}
                            data={dataSources.users.length > 0 ? dataSources.users : [{ id: 0, value: 'No data available. Please try again later' }]}
                          />
                        </Grid>
                    )}
                  
                      {/* Date Fields - Split on Desktop */}
                      <Grid item xs={12} md={6}>
                        <FormField
                          type="datepicker"
                          placeholder="Start Date"
                          name="start_time"
                          register={register}
                          getValues={getValues}
                          setValue={setValue}
                          error={errors.start_time}
                        />
                      </Grid>
                  
                      <Grid item xs={12} md={6}>
                        <FormField
                          type="datepicker"
                          placeholder="End Date"
                          name="end_time"
                          register={register}
                          getValues={getValues}
                          setValue={setValue}
                          error={errors.end_time}
                        />
                      </Grid>
                    </DetailGrid>
                </SectionContainer>
              )}

              {activeSection === 2 && (
                <>
                  <SectionContainer title="Targeting Type">
                  <DetailGrid>
                  {/* Location */}
                  <Grid item xs={12}>
                      <FormField
                            type="select"
                            placeholder="Locations"
                            name="location"
                            register={register}
                            getValues={getValues}
                            setValue={setValue}
                            onChange={handleSelectChange}
                            error={Array.isArray(errors.location)?errors.location[0]:errors.location}
                            data={dataSources.location.length > 0 ? dataSources.location : [{ id: 0, city: 'No data available. Please try again later' }]}
                        />
                    </Grid>

                    {/* Age */}
                    <Grid item xs={12} md={6}>
                      <FormField
                            type="select"
                            placeholder="Age Range"
                            name="age"
                            register={register}
                            getValues={getValues}
                            setValue={setValue}
                            onChange={handleSelectChange}
                            error={Array.isArray(errors.age)?errors.age[0]:errors.age}
                            data={dataSources.ages.length > 0 ? dataSources.ages : [{ id: 0, value: 'No data available. Please try again later' }]}
                        />
                    </Grid>
                    
                    {/* Exchange */}
                    <Grid item xs={12} md={6}>                      
                      <FormField
                            type="select"
                            placeholder="Exchange"
                            name="exchange"
                            register={register}
                            getValues={getValues}
                            setValue={setValue}
                            error={Array.isArray(errors.exchange)?errors.exchange[0]:errors.exchange}
                            data={dataSources.exchange.length > 0 ? dataSources.exchange : [{ id: 0, value: 'No data available. Please try again later' }]}
                        />
                    </Grid>

                    {/* Langugage */}
                    <Grid item xs={12} md={4}>
                        <FormField
                            type="select"
                            placeholder="Language"
                            name="language"
                            register={register}
                            getValues={getValues}
                            setValue={setValue}
                            error={Array.isArray(errors.language)?errors.language[0]:errors.language}
                            data={dataSources.language.length > 0 ? dataSources.language : [{ id: 0, value: 'No data available. Please try again later' }]}
                        />
                      </Grid>

                    {/* Viewability*/}
                    <Grid item xs={12} md={4}>
                      <FormField
                          type="select"
                          placeholder="Viewability"
                          name="viewability"
                          register={register}
                          getValues={getValues}
                          setValue={setValue}
                          error={Array.isArray(errors.viewability)?errors.viewability[0]:errors.viewability}
                          data={dataSources.viewability.length > 0 ? dataSources.viewability : [{ id: 0, value: 'No data available. Please try again later' }]}
                          multiple={false}
                          />
                    </Grid>

                    {/* Brandsafety*/}
                    <Grid item xs={12} md={4}>
                      <FormField
                          type="select"
                          placeholder="Brand Safety"
                          name="brand_safety"
                          register={register}
                          getValues={getValues}
                          setValue={setValue}
                          error={Array.isArray(errors.brand_safety)?errors.brand_safety[0]:errors.brand_safety}
                          data={dataSources.brand_safety.length > 0 ? dataSources.brand_safety : [{ id: 0, value: 'No data available. Please try again later' }]}
                          multiple={false}
                          />
                    </Grid>
                    </DetailGrid>
                  </SectionContainer>
                  <SectionContainer title="Device & Environment">
                    {/* Device */}
                    <DetailGrid>
                      <Grid item xs={12} md={6}>
                        <FormField
                            type="select"
                            placeholder="Devices"
                            name="device"
                            register={register}
                            getValues={getValues}
                            setValue={setValue}
                            error={Array.isArray(errors.device)?errors.device[0]:errors.device}
                            data={dataSources.devices.length > 0 ? dataSources.devices : [{ id: 0, value: 'No data available. Please try again later' }]}
                          />
                      </Grid>
                    
                    {/* Environment */}
                    <Grid item xs={12} md={6}>
                        <FormField
                            type="select"
                            placeholder="Environments"
                            name="environment"
                            register={register}
                            getValues={getValues}
                            setValue={setValue}
                            error={Array.isArray(errors.environment)?errors.environment[0]:errors.environment}
                            data={dataSources.environment.length > 0 ? dataSources.environment : [{ id: 0, value: 'No data available. Please try again later' }]}
                        />
                    </Grid>

                     {/* Carrier */}
                     <Grid item xs={12} md={6}>
                      <FormField
                          type="select"
                          placeholder="Carrier"
                          name="carrier"
                          register={register}
                          getValues={getValues}
                          setValue={setValue}
                          error={Array.isArray(errors.carrier)?errors.carrier[0]:errors.carrier}
                          data={dataSources.carrier.length > 0 ? dataSources.carrier : [{ id: 0, value: 'No data available. Please try again later' }]}
                      />
                    </Grid>

                    {/* DevicePrice */}
                    <Grid item xs={12} md={6}>
                      <FormField
                          type="select"
                          placeholder="DevicePrice"
                          name="device_price"
                          register={register}
                          getValues={getValues}
                          setValue={setValue}
                          error={Array.isArray(errors.device_price)?errors.device_price[0]:errors.device_price}
                          data={dataSources.device_price.length > 0 ? dataSources.device_price : [{ id: 0, value: 'No data available. Please try again later' }]}
                      />
                    </Grid>
                    </DetailGrid>
                  </SectionContainer>
                </>
              )}

              {activeSection === 3 && (
                <>
                <SectionContainer title="Interest">
                  <DetailGrid>
                    {dataSources.interest_category.map((interestCategory)=>{
                      return(
                          <>
                            <Grid item xs={12} md={6} key={(interestCategory as CommonSelectResponse).id}>
                              <TextField
                                fullWidth
                                label="Interest Category"
                                variant="outlined"
                                value={(interestCategory as CommonSelectResponse).label}
                                InputProps={{ readOnly: true }}
                              />
                            </Grid>
                        
                            <Grid item xs={12} md ={6}>
                              <FormField
                                type="select"
                                placeholder="SubCategory"
                                name={`target_type_${(interestCategory as CommonSelectResponse).id}`}
                                register={register}
                                getValues={getValues}
                                setValue={setValue}
                                onChange={handleSelectChange}
                                error={Array.isArray(errors.target_type) ? errors.target_type[0] : errors.target_type}
                                data={
                                  dataSources.interest.length > 0
                                      ? dataSources.interest.filter((interest) => (interest as Interest).category === (interestCategory as CommonSelectResponse).label)
                                    : [{ id: 0, category: "No data available. Please select Interest" }]
                                }
                              />
                            </Grid>
                          </>
                      )
                    })}
                    </DetailGrid>
                  </SectionContainer>
                  {targetType &&
                    <SectionContainer title="Interest Targeting">
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                {targetType &&
                                  <TargetType 
                                    targetType={targetType} 
                                    isRemovable={isEditable} 
                                />
                                }
                            </Grid>
                        </Grid>
                    </SectionContainer>
                  }
                </>
              )}

              {activeSection === 4 && (
                <>
                  <SectionContainer title="Budget & Bidding">
                    <DetailGrid>
                      {/* Total Budget */}
                      <Grid item xs={12} md = {6}>
                        <FormField
                            type="number"
                            placeholder="Total Budget"
                            name="total_budget"
                            valueAsNumber={true}
                            register={register}
                            setValue={setValue}
                            getValues={getValues}
                            error={Array.isArray(errors.total_budget)?errors.total_budget[0]:errors.total_budget}
                        />
                      </Grid>
                      {/* Unit Rate*/}
                      <Grid item xs={12} md={6}>
                        <FormField
                            type="number"
                            placeholder="Unit Rate"
                            name="unit_rate"
                            valueAsNumber={true}
                            getValues={getValues}
                            setValue={setValue}
                            register={register}
                            error={Array.isArray(errors.unit_rate)?errors.unit_rate[0]:errors.unit_rate}
                            />
                      </Grid>
                      {/* Buy Type*/}
                      <Grid item xs={12}>
                        <FormField
                            type="select"
                            placeholder="Buy Type"
                            name="buy_type"
                            register={register}
                            getValues={getValues}
                            setValue={setValue}
                            error={errors.buy_type}
                            data={filteredBuyTypeList.length > 0 ? filteredBuyTypeList : [{ id: 0, value: 'No data available. Please try again later' }]}
                            multiple={false}
                            />
                      </Grid>
                    </DetailGrid>
                  </SectionContainer>
                  <SectionContainer title="Ad Details">
                    <DetailGrid>
                        {/* Landing Page */}
                        <Grid item xs={12}>
                        <FormField
                            type="text"
                            placeholder="Landing Page"
                            name="landing_page"
                            register={register}
                            getValues={getValues}
                            setValue={setValue}
                            error={errors.landing_page}
                            data={undefined}
                        />
                      </Grid>

                      {/* Tag & Tracker */}
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
                      
                      {/* Image Upload */}
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
                      ):
                      (
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
                </>
              )}

              {activeSection === 5 && (
                <>
                  <CampaignReview 
                    title="Campaign Review"
                    fields={utils.reviewFields}
                    targetType={targetType}
                    dataSources={dataSources}
                    getValues={getValues}
                  />
                  <Box sx={{ textAlign: "center", mt: 3 }}>
                  {!isPending ? (
                        <Box sx={{ textAlign: "center", mt: 3 }}>
                          <Button sx={{borderRadius:0.75}} variant="contained" color="primary" type="submit">
                            {isEditable?"Update Campaign" : "Create Campaign"}
                          </Button>
                        </Box>
                  ):(
                    <Box sx={{ textAlign: "center", mt: 3 }}>
                      <Box sx={{ marginLeft: 2 }}>
                          <CircularProgress />
                        </Box>
                      </Box>
                  )}
                  </Box>
                </>
              )}
            
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
                <Button variant="outlined" onClick={prevSection} disabled={activeSection === 0}>
                  Previous
                </Button>
                {activeSection < 5 && (
                  <Button variant="contained" color="primary" onClick={nextSection}>
                    {activeSection === 4 ? "Review" : "Next"}
                  </Button>
                )}
              </Box>
            </Box>

            <>
              {errors.root ? <Alert color="error">{errors.root.message}</Alert> : null}
              {isCampaignCreated ? <Alert sx={{margin:2}} color="success">Campaign created successfully!</Alert> : null}
            </>
          </form>
        </Box>

        {/* Right Section (Chart) */}
        <Box
          sx={{
            flex: { md: "1", lg: "1" },
            display: { xs: "none", sm: "none", md: "flex" },
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            bgcolor: "background.paper",
            p: 2,
            border:1,
            borderColor: "grey.200",
            position: "sticky",
            top: '72px',
            alignSelf: 'flex-start',
          }}
        >
          <ImpressionComponent title= " Campaign Population Breakdown" targetPopulation={targetPopulation} totalPopulation={totalPopulation} />
        </Box>
      </Box>
    );
  }

  