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
import CircularProgress from '@material-ui/core/CircularProgress';
import Fade from '@material-ui/core/Fade';

import DiffGraphVis from './DiffGraphVis';

const styles = theme => ({
    root: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    },
    button: {
      margin: theme.spacing.unit * 2,
    },
    
  });

class GraphUI extends Component {
    constructor(props) {
        super(props);

        this.state = {
            uploading: false,
            file: {},
            detected_genes: {}
        };
    }

    handleUploadClicked = () => {
        console.log("analyze clicked");

        this.setState({ uploading: true })

        const formData = new FormData();
        formData.append('file', this.state.file)

        fetch("http://localhost:5000"+ '/paper/analyze', {
            method: 'POST',
            body: formData
        })
        .then( (response) => {
            return response.json()    
        })
        .then( (json) => {
          this.setState({
             uploading: false,
             detected_genes: json
          })
          console.log('parsed json', json)
        })
        .catch( (ex) => {
          console.log('parsing failed', ex)
        })
    }

    handleInputOnChange = (event) => {
        console.log("handleInputOnChange");
        console.log(event.target.files[0]);

        this.setState({ file: event.target.files[0] })
    }

    render() {
        const { classes } = this.props;
        const { uploading } = this.state;

        const genes = this.state.detected_genes.detected_genes;
        const classified = this.state.detected_genes.classified_gene_interaction;
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
                    <input onChange={this.handleInputOnChange} type="file" id="upload-file" accept=".pdf,.txt"/>
                    <Button onClick={this.handleUploadClicked}>
                        Analyze File
                    </Button>

                     <Fade
                        className={classes.placeholder}
                        in={uploading}
                        style={{
                        transitionDelay: uploading ? '800ms' : '0ms',
                        }}
                        unmountOnExit
                    >
                        <CircularProgress />
                    </Fade>

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
                <h2> Red - Not found in the paper</h2>
                <DiffGraphVis genes={genes} classified={classified}/>
    
            </div>
            
        );
    }
    
}
export default withStyles(styles)(GraphUI);