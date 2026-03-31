import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Drawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import MenuIcon from '@mui/icons-material/Menu';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';

const linkStyles = {
  color: 'inherit',
  textDecoration: 'none',
};

export default function NavBar({ activePage, pageLinks = [] }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [menuAnchors, setMenuAnchors] = useState({});

  const toggleDrawer = () => {
    setMobileOpen((open) => !open);
  };

  const openMenu = (key, event) => {
    setMenuAnchors((current) => ({ ...current, [key]: event.currentTarget }));
  };

  const closeMenu = (key) => {
    setMenuAnchors((current) => ({ ...current, [key]: null }));
  };

  const resolveIsActive = (page, isActive) => {
    if (isActive) {
      return true;
    }

    return activePage === page.key || activePage === page.label || activePage === page.to;
  };

  const shouldRenderDropdown = (page) =>
    ['farms', 'fields'].includes(page.key) && Array.isArray(page.items) && page.items.length > 0;

  const navItems = pageLinks.map((page) => (
    shouldRenderDropdown(page) ? (
      <Box key={page.to} sx={{ display: { xs: 'none', md: 'inline-flex' } }}>
        <Button
          color="inherit"
          endIcon={<ArrowDropDownIcon />}
          onClick={(event) => openMenu(page.key, event)}
          sx={{
            borderBottom: 2,
            borderColor: menuAnchors[page.key] ? 'secondary.main' : 'transparent',
            borderRadius: 0,
            fontWeight: menuAnchors[page.key] ? 700 : 500,
            mx: 0.5,
          }}
        >
          {page.label}
        </Button>
        <Menu
          anchorEl={menuAnchors[page.key]}
          onClose={() => closeMenu(page.key)}
          open={Boolean(menuAnchors[page.key])}
        >
          <MenuItem component={NavLink} onClick={() => closeMenu(page.key)} to={page.to}>
            All {page.label}
          </MenuItem>
          {page.items.map((item) => (
            <MenuItem
              component={NavLink}
              key={item.to}
              onClick={() => closeMenu(page.key)}
              to={item.to}
            >
              {item.label}
            </MenuItem>
          ))}
        </Menu>
      </Box>
    ) : (
      <NavLink key={page.to} to={page.to} style={linkStyles} end={page.to === '/'}>
        {({ isActive }) => {
          const selected = resolveIsActive(page, isActive);

          return (
            <Button
              color="inherit"
              sx={{
                borderBottom: 2,
                borderColor: selected ? 'secondary.main' : 'transparent',
                borderRadius: 0,
                display: { xs: 'none', md: 'inline-flex' },
                fontWeight: selected ? 700 : 500,
                mx: 0.5,
              }}
            >
              {page.label}
            </Button>
          );
        }}
      </NavLink>
    )
  ));

  const drawerItems = (
    <Box onClick={toggleDrawer} sx={{ textAlign: 'center', width: 260 }}>
      <Typography sx={{ my: 2 }} variant="h6">
        GDD Calculator
      </Typography>
      <List>
        {pageLinks.map((page) => (
          <Box key={page.to}>
            <ListItem disablePadding>
              <NavLink to={page.to} style={linkStyles}>
                {({ isActive }) => (
                  <ListItemButton selected={resolveIsActive(page, isActive)} sx={{ width: 260 }}>
                    <ListItemText primary={page.label} />
                  </ListItemButton>
                )}
              </NavLink>
            </ListItem>
            {shouldRenderDropdown(page) &&
              page.items.map((item) => (
                <ListItem disablePadding key={item.to}>
                  <NavLink to={item.to} style={linkStyles}>
                    {({ isActive }) => (
                      <ListItemButton selected={isActive} sx={{ pl: 4, width: 260 }}>
                        <ListItemText primary={item.label} />
                      </ListItemButton>
                    )}
                  </NavLink>
                </ListItem>
              ))}
          </Box>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            aria-label="open navigation menu"
            color="inherit"
            edge="start"
            onClick={toggleDrawer}
            sx={{ display: { md: 'none' }, mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography component="div" sx={{ flexGrow: 1, fontWeight: 700 }} variant="h6">
            GDD Calculator
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>{navItems}</Box>
        </Toolbar>
      </AppBar>
      <Drawer
        anchor="left"
        ModalProps={{ keepMounted: true }}
        onClose={toggleDrawer}
        open={mobileOpen}
        sx={{ display: { xs: 'block', md: 'none' } }}
      >
        {drawerItems}
      </Drawer>
    </Box>
  );
}
