import React, { Component, Fragment } from 'react';

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles'
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';

const styles = {

};

class GraphUI extends Component {
    constructor(props) {
        super(props);

        this.state = {

        };
    }

    render() {
        //const { classes } = this.prop

        return (
            <div >
                <AppBar position="static">
                    <Toolbar>
                        <IconButton  color="inherit" aria-label="Menu">
                            <MenuIcon />
                        </IconButton>
                        <Typography variant="h6" color="inherit" >
                            Interactions
                        </Typography>
                    </Toolbar>
                </AppBar>
                <Paper>
                    <input type="file" id="upload-file" />
                    <Button>
                        Analyze File
                    </Button>

                    <ExpansionPanel>
                        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
                            <Typography >Visualization Settings</Typography>
                        </ExpansionPanelSummary>
                        <ExpansionPanelDetails>
                            <Button>
                                Setting 1
                            </Button>
                        </ExpansionPanelDetails>
                    </ExpansionPanel>
                    
                </Paper>
    
            </div>
            
        );
    }
    
}
export default withStyles(styles)(GraphUI);