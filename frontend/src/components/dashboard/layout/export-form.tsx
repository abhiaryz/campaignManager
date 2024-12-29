import Box from '@mui/material/Box';
import Popover from '@mui/material/Popover';
import Typography from '@mui/material/Typography';
import * as React from 'react';

import { Button, Card, CardContent, CardHeader, FormControl, TextField } from '@mui/material';
import { X } from '@phosphor-icons/react/dist/ssr';
import { ArrowFatUp } from '@phosphor-icons/react/dist/ssr/ArrowFatUp';

  export interface UserPopoverProps {
    anchorEl: Element | null;
    onClose: () => void;
    open: boolean;
  }

  
  export function ExportFormPopover({ anchorEl, onClose, open }: UserPopoverProps): React.JSX.Element {
  
    return (
      <Popover
        anchorEl={anchorEl}
        anchorOrigin={{ horizontal: 'center', vertical: 'center' }}
        onClose={onClose}
        open={open}
        slotProps={{ paper: { sx: { width: '512px' } } }}
      >
        <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Card>
            <Button
              onClick={onClose}
              sx={{ position: 'absolute', top: 8, right: 8 }} startIcon={<X fontSize="var(--icon-fontSize-md)" />} 
            />
            <CardHeader title="Location Setting" />
            <CardContent>
              <Typography variant="body2">Select location for the campaign:</Typography>
              <FormControl fullWidth>
                <TextField id="outlined-basic" label="Outlined" variant="outlined" />
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
                    <Button color="inherit" startIcon={<ArrowFatUp fontSize="var(--icon-fontSize-md)" />} variant="contained">Export</Button>
                </div>
              </FormControl>
            </CardContent>
          </Card>
        </Box>
      </Popover>
    );
  }
  