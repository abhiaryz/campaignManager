"use client"
import { Button } from '@mui/material';
import { Stack, Box } from '@mui/system';
import React from 'react';
import { ExportFormPopover } from '../layout/export-form';
import { Download as DownloadIcon } from '@phosphor-icons/react/dist/ssr/Download';
import { usePopover } from '@/hooks/use-popover';

const ExportForm: React.FC = () => {
    const exportPopOver = usePopover<HTMLDivElement>();

    return (
        <Stack sx={{ alignItems: 'center' }} direction="row" spacing={1}>
            <Button  onClick={exportPopOver.handleOpen} color="inherit" startIcon={<DownloadIcon fontSize="var(--icon-fontSize-md)" />}>
              Export
            </Button>
            <Box
              sx={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                backdropFilter: 'blur(5px)',
                zIndex: exportPopOver.open ? 1 : -1,
                opacity: exportPopOver.open ? 1 : 0,
                transition: 'opacity 0.3s ease',
              }}
            />
            <ExportFormPopover anchorEl={exportPopOver.anchorRef.current} onClose={exportPopOver.handleClose} open={exportPopOver.open} />
          </Stack>
    );
};

export default ExportForm;