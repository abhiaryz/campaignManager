"use client"
import { Box, Card, CardContent, CardHeader, FormControl, TextField } from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import Typography from '@mui/material/Typography';
import * as React from 'react';

export default function BudgetBidding(): React.JSX.Element {

  const [age] = React.useState('');

  return (
    <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Card>
            <CardHeader title="Budget & Bidding" />
            <CardContent>
              <Typography variant="body2">Select location for the campaign:</Typography>
              <FormControl fullWidth>
                <TextField id="outlined-basic" label="Outlined" variant="outlined" />
              </FormControl>
            </CardContent>
            <CardContent>

            <Typography variant="body2">Select location for the campaign:</Typography>
              <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Age</InputLabel>
                <Select
                  labelId="demo-simple-select-label"
                  id="demo-simple-select"
                  value={age}
                  label="Age"
                >
                  <MenuItem value={10}>Ten</MenuItem>
                  <MenuItem value={20}>Twenty</MenuItem>
                  <MenuItem value={30}>Thirty</MenuItem>
                </Select>
              </FormControl>
              </CardContent>
          </Card>
        </Box>
  );
}