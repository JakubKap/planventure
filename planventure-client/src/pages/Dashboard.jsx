import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Button,
  Card,
  CardContent,
  Avatar,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Add as AddIcon,
  Map as MapIcon,
  CalendarToday as CalendarIcon,
  LocationOn as LocationIcon,
  TrendingUp as TrendingUpIcon,
  Flight as FlightIcon,
  Hotel as HotelIcon,
  Restaurant as RestaurantIcon,
  Edit as EditIcon
} from '@mui/icons-material';
import PropTypes from 'prop-types';
import TripList from '../components/trips/TripList';
import { useAuth } from '../hooks/useAuth';
import travelingSvg from '../assets/undraw_traveling_yhxq.svg';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [trips, setTrips] = useState([]);

  // Mock data for demonstration - in a real app, this would come from an API
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setTrips([
        {
          id: 1,
          title: 'Tokyo Adventure',
          destination: 'Tokyo, Japan',
          startDate: '2024-06-15',
          endDate: '2024-06-25',
          status: 'upcoming'
        },
        {
          id: 2,
          title: 'Paris Getaway',
          destination: 'Paris, France',
          startDate: '2024-04-10',
          endDate: '2024-04-18',
          status: 'completed'
        }
      ]);
    }, 1000);
  }, []);

  const upcomingTrips = trips.filter(trip => trip.status === 'upcoming');
  const completedTrips = trips.filter(trip => trip.status === 'completed');

  const StatCard = ({ title, value, icon, color }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Avatar sx={{ bgcolor: color, mr: 2 }}>
            {icon}
          </Avatar>
          <Box>
            <Typography variant="h4" component="div">
              {value}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {title}
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  StatCard.propTypes = {
    title: PropTypes.string.isRequired,
    value: PropTypes.number.isRequired,
    icon: PropTypes.element.isRequired,
    color: PropTypes.string.isRequired,
  };

  const QuickActions = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Quick Actions
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Button
              fullWidth
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => navigate('/trips/new')}
              sx={{ mb: 1 }}
            >
              New Trip
            </Button>
          </Grid>
          <Grid item xs={6}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<MapIcon />}
              onClick={() => navigate('/trips')}
            >
              View All Trips
            </Button>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );

  const RecentTrips = () => (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            Recent Trips
          </Typography>
          <Button size="small" onClick={() => navigate('/trips')}>
            View All
          </Button>
        </Box>
        <List>
          {trips.slice(0, 3).map((trip, index) => (
            <div key={trip.id}>
              <ListItem
                secondaryAction={
                  <Box>
                    <Tooltip title="Edit">
                      <IconButton edge="end" onClick={() => navigate(`/trips/${trip.id}/edit`)}>
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="View Details">
                      <IconButton edge="end" onClick={() => navigate(`/trips/${trip.id}`)}>
                        <MapIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
                }
              >
                <ListItemAvatar>
                  <Avatar sx={{ bgcolor: trip.status === 'upcoming' ? 'primary.main' : 'success.main' }}>
                    <LocationIcon />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={trip.title}
                  secondary={
                    <Box>
                      <Typography variant="body2" component="span">
                        {trip.destination}
                      </Typography>
                      <br />
                      <Typography variant="caption" color="text.secondary">
                        {new Date(trip.startDate).toLocaleDateString()} - {new Date(trip.endDate).toLocaleDateString()}
                      </Typography>
                      <Chip
                        size="small"
                        label={trip.status}
                        color={trip.status === 'upcoming' ? 'primary' : 'success'}
                        sx={{ ml: 1 }}
                      />
                    </Box>
                  }
                />
              </ListItem>
              {index < trips.slice(0, 3).length - 1 && <Divider />}
            </div>
          ))}
        </List>
        {trips.length === 0 && (
          <Box sx={{ textAlign: 'center', py: 3 }}>
            <Typography variant="body2" color="text.secondary">
              No trips yet. Start planning your first adventure!
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );

  const UpcomingActivities = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Upcoming Activities
        </Typography>
        <List>
          <ListItem>
            <ListItemAvatar>
              <Avatar sx={{ bgcolor: 'warning.main' }}>
                <FlightIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary="Flight to Tokyo"
              secondary="June 15, 2024 • 10:30 AM"
            />
          </ListItem>
          <Divider />
          <ListItem>
            <ListItemAvatar>
              <Avatar sx={{ bgcolor: 'info.main' }}>
                <HotelIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary="Check-in at Tokyo Hotel"
              secondary="June 15, 2024 • 3:00 PM"
            />
          </ListItem>
          <Divider />
          <ListItem>
            <ListItemAvatar>
              <Avatar sx={{ bgcolor: 'success.main' }}>
                <RestaurantIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText
              primary="Dinner at Sushi Restaurant"
              secondary="June 15, 2024 • 7:00 PM"
            />
          </ListItem>
        </List>
      </CardContent>
    </Card>
  );

  const WelcomeMessage = () => (
    <Box
      sx={{
        textAlign: 'center',
        py: 4,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2
      }}
    >
      <img
        src={travelingSvg}
        alt="Start your journey"
        style={{
          maxWidth: '200px',
          width: '100%',
          height: 'auto',
          marginBottom: '1rem'
        }}
      />
      <Typography variant="h6" component="h2" gutterBottom>
        Ready to start your first adventure?
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ maxWidth: '400px', mb: 2 }}>
        Create your first trip and let us help you organize everything from destinations to activities.
      </Typography>
      <Button
        variant="contained"
        startIcon={<AddIcon />}
        onClick={() => navigate('/trips/new')}
      >
        Plan Your First Trip
      </Button>
    </Box>
  );

  const ErrorState = () => (
    <Box
      sx={{
        textAlign: 'center',
        py: 4,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2
      }}
    >
      <img
        src={travelingSvg}
        alt="Error loading trips"
        style={{
          maxWidth: '200px',
          width: '100%',
          height: 'auto',
          marginBottom: '1rem',
          opacity: 0.7
        }}
      />
      <Typography variant="h6" component="h2" gutterBottom>
        Oops! Our compass is spinning! 🧭
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ maxWidth: '400px', mb: 2 }}>
        We&apos;re having trouble loading your adventures. Try refreshing the page.
      </Typography>
      <Button
        variant="contained"
        onClick={() => window.location.reload()}
      >
        Try Again
      </Button>
    </Box>
  );

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      {/* Welcome Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome back, {user?.email?.split('@')[0] || 'Traveler'}! 🌍
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Ready to plan your next adventure? Here&apos;s your travel overview.
        </Typography>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Trips"
            value={trips.length}
            icon={<MapIcon />}
            color="primary.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Upcoming"
            value={upcomingTrips.length}
            icon={<CalendarIcon />}
            color="warning.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Completed"
            value={completedTrips.length}
            icon={<TrendingUpIcon />}
            color="success.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="This Year"
            value={trips.filter(trip => new Date(trip.startDate).getFullYear() === new Date().getFullYear()).length}
            icon={<LocationIcon />}
            color="info.main"
          />
        </Grid>
      </Grid>

      {/* Main Content Grid */}
      <Grid container spacing={3}>
        {/* Quick Actions */}
        <Grid item xs={12} md={4}>
          <QuickActions />
        </Grid>

        {/* Recent Trips */}
        <Grid item xs={12} md={8}>
          <RecentTrips />
        </Grid>

        {/* Upcoming Activities */}
        <Grid item xs={12}>
          <UpcomingActivities />
        </Grid>
      </Grid>

      {/* Full Trip List (if needed) */}
      {trips.length > 3 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom sx={{ mt: 4 }}>
            All Your Trips
          </Typography>
          <Paper elevation={2} sx={{ p: 3 }}>
            <TripList
              WelcomeMessage={WelcomeMessage}
              ErrorState={ErrorState}
            />
          </Paper>
        </Box>
      )}
    </Box>
  );
};

export default Dashboard;
