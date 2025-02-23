import * as React from 'react';
import { IconButton, Menu, MenuItem, Checkbox, ListItemText } from '@mui/material';
import { Funnel } from '@phosphor-icons/react';

interface FieldSelectorProps {
  onFieldsChange: (fields: string[]) => void;
  selectedFields: string[];
}

const AVAILABLE_FIELDS = [
  'Campaign Id',
  'Campaign Name',
  'Advertiser Name',
  'Objective',
  'Buy Type',
  'Unit Rate',
  'Budget',
  'Impression',
  'Click',
  'CTR',
  'Views',
  'VTR',
  'Status'
];

export const FieldSelector: React.FC<FieldSelectorProps> = ({ onFieldsChange, selectedFields }) => {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleToggle = (field: string) => {
    const currentIndex = selectedFields.indexOf(field);
    const newSelected = [...selectedFields];

    if (currentIndex === -1) {
      newSelected.push(field);
    } else {
      newSelected.splice(currentIndex, 1);
    }

    onFieldsChange(newSelected);
  };

  return (
    <>
      <IconButton
        aria-label="show columns"
        onClick={handleClick}
        size="small"
      >
        <Funnel weight="bold" />
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        slotProps={{
          paper: {
            style: {
              maxHeight: 300,
              width: 200,
            },
          },
        }}
      >
        {AVAILABLE_FIELDS.map((field) => (
          <MenuItem 
            key={field} 
            onClick={() => handleToggle(field)}
            dense
          >
            <Checkbox 
              checked={selectedFields.indexOf(field) > -1}
              size="small"
            />
            <ListItemText primary={field} />
          </MenuItem>
        ))}
      </Menu>
    </>
  );
}; 