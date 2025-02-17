'use client';

import { useAuth } from '@/hooks/use-auth';
import { paths } from '@/paths';
import { User } from '@/types/auth';
import { signUpSchema } from '@/types/schema';
import { zodResolver } from '@hookform/resolvers/zod';
import { Box, CircularProgress, Grid } from '@mui/material';
import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import RouterLink from 'next/link';
import { useRouter } from 'next/navigation';
import * as React from 'react';
import { useForm } from 'react-hook-form';
import { authClient } from '../../lib/auth-client';
import FormField from '../dashboard/layout/form-field';

export function SignUpForm(): React.JSX.Element {
  const router = useRouter();

  const { checkSession } = useAuth();

    const [isPending, setIsPending] = React.useState<boolean>(false);
    const [isUserCreated,setIsUserCreated] = React.useState<boolean>(false);

    const {
      register,
      handleSubmit,
      setError,
      formState: { errors },
    } = useForm<User>({ resolver: zodResolver(signUpSchema) });

  const onSubmit = React.useCallback(
    async (values: User): Promise<void> => {
      setIsPending(true);
      try {
        const result = await authClient.signUp(values);
        if (result) {
          setIsUserCreated(true);
          await checkSession?.();
          setTimeout(()=>{
            router.push(paths.auth.signIn);
          },100)
        }
      } catch (error:any) {
        setError('root', { type: 'server', message: error.message});
      } finally {
        setIsPending(false);
      }
    },
    [checkSession, router, setError]
  );

  return (
    <Stack spacing={3}>
      <Stack spacing={1}>
        <Typography variant="h4">Sign up</Typography>
        <Typography color="text.secondary" variant="body2">
          Already have an account?{' '}
          <Link component={RouterLink} href="/auth/sign-in" underline="hover" variant="subtitle2">
            Sign in
          </Link>
        </Typography>
      </Stack>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Stack spacing={2}>
          {/* First Name */}
          <Grid item xs={12} md={6} mb={1}>
            <Box sx={{ minWidth: 120 }}>
            <FormField
                type="text"
                placeholder="First Name"
                name="first_name"
                register={register}
                error={errors.first_name}
            />
            </Box>
          </Grid>

          {/* Last Name */}
          <Grid item xs={12} md={6} mb={1}>
              <Box sx={{ minWidth: 120 }}>
              <FormField
                  type="text"
                  placeholder="Last Name"
                  name="last_name"
                  register={register}
                  error={errors.last_name}
              />
              </Box>
            </Grid>

          {/* Email */}
          <Grid item xs={12} md={6} mb={1}>
            <Box sx={{ minWidth: 120 }}>
            <FormField
                type="email"
                placeholder="Email"
                name="email"
                register={register}
                error={errors.email}
            />
            </Box>
          </Grid>
          {/* Password */}
          <Grid item xs={12} md={6} mb={1}>
            <Box sx={{ minWidth: 120 }}>
              <FormField
                  type="password"
                  placeholder="Password"
                  name="password"
                  register={register}
                  error={errors.password}
              />
            </Box>
          </Grid>
          
          {/* Company Name */}
          <Grid item xs={12} md={6} mb={1}>
            <Box sx={{ minWidth: 120 }}>
            <FormField
                type="text"
                placeholder="Company Name"
                name="company_name"
                register={register}
                error={errors.company_name}
            />
            </Box>
          </Grid>

          {/* GST */}
          <Grid item xs={12} md={6} mb={1}>
            <Box sx={{ minWidth: 120 }}>
            <FormField
                type="text"
                placeholder="GST"
                name="gst"
                register={register}
                error={errors.gst}
            />
            </Box>
          </Grid>

          {/** Terms */}
          <Grid item xs={12} md={6} mb={1}>
            <Box sx={{ minWidth: 120 }}>
              <FormField
                  type="checkbox"
                  placeholder="Terms & Conditions"
                  name="terms"
                  register={register}
                  error={errors.terms}
              />
            </Box>
          </Grid>

          {errors.root ? <Alert color="error">{errors.root.message}</Alert> : null}
          {!isPending && (
            <Box sx={{ textAlign: "center", mt: 3 }}>
              <Button variant="contained" color="primary" type="submit">
              Sign up
              </Button>
            </Box>
          )}
          
          {isPending && (
            <Box sx={{ textAlign: "center", mt: 3 }}>
              <Box sx={{ marginLeft: 2 }}>
                  <CircularProgress />
                </Box>
              </Box>
          )}    
          {isUserCreated ? <Alert color="success">User created successfully</Alert> : null} 
        </Stack>
      </form>
    </Stack>
  );
}