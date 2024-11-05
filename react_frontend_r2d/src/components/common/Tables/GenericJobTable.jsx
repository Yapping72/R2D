import React, { useState, useEffect } from 'react';
import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TablePagination, TableSortLabel, Typography, IconButton, Chip, CircularProgress, Tooltip, Collapse } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useAlert } from '../Alerts/AlertContext';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';

// Compares two items based on the orderBy property in descending order
function descendingComparator(a, b, orderBy) {
    // If the orderBy property of b is less than a, place b before a (-1)
    if (b[orderBy] < a[orderBy]) {
        return -1;
    }
    // If the orderBy property of b is greater than a, place a before b (1)
    if (b[orderBy] > a[orderBy]) {
        return 1;
    }
    // If equal, no change in order (0)
    return 0;
}

// Generates a comparator function for sorting based on order and orderBy parameters
function getComparator(order, orderBy) {
    // If descending order is requested, use descendingComparator directly
    return order === 'desc'
        ? (a, b) => descendingComparator(a, b, orderBy)
        // If ascending order is requested, reverse the result of descendingComparator
        : (a, b) => -descendingComparator(a, b, orderBy);
}

/**
 * Renders a status chip with a tooltip based on the status.
 * 
 * Supported statuses:
 * - Draft: Ready to submit.
 * - Queued: Queued and ready for processing.
 * - Submitted: Successfully submitted, waiting for processing.
 * - Error Failed to Submit: Errors occurred during submission.
 * - Error Failed to Process: Errors occurred during processing.
 * - Completed: Successfully completed.
 * - Processing: Currently being processed.
 * - Job Aborted: Job has been aborted.
 *
 * @param {string} status - The current status of a job or request.
 * @returns {JSX.Element|null} A Material-UI Chip wrapped in a Tooltip if a valid status, otherwise null.
 */
   export const renderStatus = (status) => {
        switch (status) {
            case "Draft":
                return (
                    <Tooltip title="Ready to submit" variant='outlined'>
                        <Chip label={status} />
                    </Tooltip>
                );
            case "Queued":
                return (
                    <Tooltip title="Queued and ready to submit">
                        <Chip label={status} />
                    </Tooltip>
                );
            case "Submitted":
                return (
                    <Tooltip title="Request submitted successfully. Your request will be processed once resources are available.">
                        <Chip label={status} color='primary' variant='outlined' />
                    </Tooltip>
                );
            case "Error Failed to Submit":
                return (
                    <Tooltip title="Errors were occurred while submitting your request. 
                    Verify that your job parameters are valid, and resubmit again.">
                        <Chip label="Submission Error" color='error' />
                    </Tooltip>
                );
            case "Error Failed to Process":
                return (
                    <Tooltip title="Errors were encountered while processing your request.
                    Verify that your job parameters are valid, and resubmit again.">
                        <Chip label="Processing Error" color='error' />
                    </Tooltip>
                );
            case "Completed":
                return (
                    <Tooltip title="Your request has been completed successfully.">
                        <Chip label={status} color='success' />
                    </Tooltip>
                );
            case "Processing":
                return (
                    <Tooltip title="Your request is currently being processed. Please wait while we generate your diagrams.">
                        <Chip
                            label="Processing"
                            color='primary'
                        />
                    </Tooltip>
                );
            case "Job Aborted":
                return (
                    <Tooltip title="Your job has been successfully aborted.">
                        <Chip
                            label="Job Aborted"
                            color='warning'
                        />
                    </Tooltip>
                );
            default:
                return null;
        }
};

/**
 * Generic Job Table that renders items within the IndexedDB (repository will provide which db to retrieve from). Provides sorting and sizing.
 * @param {repository} repository Concrete Job Repository that provides a ReadAll function to retrieve all records from IndexedDB.
 * @param {buttonGroup} buttonGroup optional ButtonGroup object that implements its on OnClick functionality. Rendered for each row under the Actions column. 
 * @returns 
*/


const GenericJobTable = ({ repository, buttonGroup = null }) => {
    const [order, setOrder] = useState('desc');
    const [orderBy, setOrderBy] = useState('');
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const [topLevelJobs, setTopLevelJobs] = useState([]);
    const [expandedRows, setExpandedRows] = useState({});
    const { showAlert } = useAlert();

    useEffect(() => {
        const fetchData = async () => {
            const response = await repository.handleReadAll();
            if (response.success) {
                const jobs = response.data;

                const jobMap = {};
                jobs.forEach(job => (jobMap[job.job_id] = { ...job, children: [] }));

                const nestedJobs = [];
                jobs.forEach(job => {
                    if (job.parent_job) {
                        jobMap[job.parent_job]?.children.push(jobMap[job.job_id]);
                    } else {
                        nestedJobs.push(jobMap[job.job_id]);
                    }
                });

                setTopLevelJobs(nestedJobs);
            } else {
                showAlert('error', "We're having trouble retrieving uploaded files. Please try again shortly.");
            }
        };
        fetchData();
    }, [repository]);

    const handleExpandRow = (jobId) => {
        setExpandedRows(prev => ({ ...prev, [jobId]: !prev[jobId] }));
    };

    const handleRequestSort = (_, property) => {
        const isAsc = orderBy === property && order === 'asc';
        setOrder(isAsc ? 'desc' : 'asc');
        setOrderBy(property);
    };

    const renderNestedRows = (jobs, level = 0) => {
        return jobs.map(job => (
            <React.Fragment key={job.job_id}>
                <TableRow hover role="checkbox" tabIndex={-1}>
                    <TableCell padding="checkbox" style={{ paddingLeft: level * 20 }}>
                        {job.children.length > 0 && (
                            <IconButton
                                aria-label="expand row"
                                size="small"
                                onClick={() => handleExpandRow(job.job_id)}
                            >
                                {expandedRows[job.job_id] ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                            </IconButton>
                        )}
                    </TableCell>
                    <TableCell>{job.job_id}</TableCell>
                    <TableCell>{job.job_details}</TableCell>
                    <TableCell>{job.job_type}</TableCell>
                    <TableCell>{renderStatus(job.job_status)}</TableCell>
                    <TableCell>{job.model_name}</TableCell>
                    <TableCell>{new Date(job.last_updated_timestamp).toLocaleString()}</TableCell>
                    {buttonGroup && level === 0 && (
                        <TableCell align="left">
                            {React.cloneElement(buttonGroup, { jobStatus: job.job_status, jobId: job.job_id })}
                        </TableCell>
                    )}
                </TableRow>
                {job.children.length > 0 && (
                    <TableRow>
                        <TableCell colSpan={7} style={{ paddingBottom: 0, paddingTop: 0 }}>
                            <Collapse in={expandedRows[job.job_id]} timeout="auto" unmountOnExit>
                                <Box margin={1} style={{ paddingLeft: level * 20 }}>
                                    {renderNestedRows(job.children, level + 1)}
                                </Box>
                            </Collapse>
                        </TableCell>
                    </TableRow>
                )}
            </React.Fragment>
        ));
    };

    return (
        <Paper elevation={0} sx={{ backgroundColor: '#2c2c2c', color: '#ffffff' }}>
            <TableContainer sx={{ maxHeight: '100%' }}>
                <Table stickyHeader aria-label="job table">
                    <TableHead>
                        <TableRow sx={{ backgroundColor: '#424242' }}>
                            <TableCell sx={{ fontWeight: 'bold', color: '#e0e0e0', borderBottom: '2px solid #ffffff' }}> </TableCell>
                            <TableCell sx={{ fontWeight: 'bold', color: '#e0e0e0', borderBottom: '2px solid #ffffff' }}>Job ID</TableCell>
                            <TableCell sx={{ fontWeight: 'bold', color: '#e0e0e0', borderBottom: '2px solid #ffffff' }}>Job Details</TableCell>
                            <TableCell sx={{ fontWeight: 'bold', color: '#e0e0e0', borderBottom: '2px solid #ffffff' }}>Job Type</TableCell>
                            <TableCell sx={{ fontWeight: 'bold', color: '#e0e0e0', borderBottom: '2px solid #ffffff' }}>Job Status</TableCell>
                            <TableCell sx={{ fontWeight: 'bold', color: '#e0e0e0', borderBottom: '2px solid #ffffff' }}>Model</TableCell>
                            <TableCell sx={{ fontWeight: 'bold', color: '#e0e0e0', borderBottom: '2px solid #ffffff' }}>Last Updated</TableCell>
                            {buttonGroup && <TableCell align="center" sx={{ fontWeight: 'bold', color: '#e0e0e0', borderBottom: '2px solid #ffffff' }}>Actions</TableCell>}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {topLevelJobs.length > 0 ? (
                            renderNestedRows(topLevelJobs)
                        ) : (
                            <TableRow>
                                <TableCell colSpan={8} align="center">
                                    <Typography>No jobs found</Typography>
                                </TableCell>
                            </TableRow>
                        )}
                        <TableRow>
                            <TablePagination
                                rowsPerPageOptions={[5, 10, 25]}
                                count={topLevelJobs.length}
                                rowsPerPage={rowsPerPage}
                                page={page}
                                onPageChange={(_, newPage) => setPage(newPage)}
                                onRowsPerPageChange={(event) => {
                                    setRowsPerPage(parseInt(event.target.value, 10));
                                    setPage(0);
                                }}
                            />
                        </TableRow>
                    </TableBody>
                </Table>
            </TableContainer>
        </Paper>
    );
};
const GenericJobTableX = ({ repository, buttonGroup = null }) => {
    const [order, setOrder] = useState('desc');
    const [orderBy, setOrderBy] = useState('');
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const [data, setData] = useState([]);
    const [columns, setColumns] = useState([]);
    const { showAlert } = useAlert();
    const [showJobIds, setShowJobIds] = useState(false); // State to track visibility of job IDs

    useEffect(() => {
        const fetchData = async () => {
            const response = await repository.handleReadAll();
            if (response.success) {

                // Create two lists:
                    // 1. List of all jobs with parent id = NULL (i.e. top level jobs)
                    // 2. Key value pair of parent id to list of child jobs
                         // Note that if job1->job2 and job2->job3, then job1 should have 2 collapsible elements job2 and job3.
                         // For job2 and job3 we only need to display - Job id, job details, job type, parent job id, job status, model name and last updated timestamp
                // List 1 will be used to display the top level jobs
                // List 2 will be used to display the child jobs of each top level job
                setData(response.data);
            } else {
                showAlert('error', `We're having trouble retrieving uploaded files at the moment. Please try again shortly, or reach out to our support team for assistance. We appreciate your patience.`)
            }
        };
        fetchData();
    }, [repository]);

    useEffect(() => {
        if (data.length > 0) {
            const columnNames = Object.keys(data[0]).filter(key => key !== "content"); // Excludes content type
            setColumns(columnNames);
        }
    }, [data]);

    const handleRequestSort = (_, property) => {
        const isAsc = orderBy === property && order === 'asc';
        setOrder(isAsc ? 'desc' : 'asc');
        setOrderBy(property);
    };

    const handleChangePage = (_, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    // When visibility icon is clicked job ids are shown
    const toggleShowJobIds = () => {
        setShowJobIds(!showJobIds);
    };

    return (
        <>
            <Paper elevation={0}>
                <TableContainer sx={{ maxHeight: '100%' }}>
                    <Table stickyHeader aria-label="sticky table">
                        <TableHead>
                            <TableRow>
                                {columns.map((column) => {
                                    // Mask user_id column
                                    if (column === "user_id" || column === "parameters") {
                                        return null;
                                    }

                                    let columnName = column;
                                    // Format the timestamp columns to save space
                                    if (column === "created_timestamp") {
                                        columnName = "created_at"; // delimiters removed below
                                    } else if (column === "last_updated_timestamp") {
                                        columnName = "last_updated";
                                    }

                                    // Capitalize each word and join with non-breaking spaces
                                    let columnHeader = columnName.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join('\u00A0');

                                    // Render the table header
                                    return (
                                        <TableCell
                                            key={column}
                                            align="left"
                                            sortDirection={orderBy === column ? order : 'asc'}
                                            sx={{
                                                fontWeight: 'bold',
                                                fontSize: '17px', // Set column name size size
                                                backgroundColor: 'black',
                                            }}
                                        >
                                            <TableSortLabel
                                                active={orderBy === column}
                                                direction={orderBy === column ? order : 'desc'}
                                                onClick={(event) => handleRequestSort(event, column)}
                                            >
                                                {columnHeader}
                                            </TableSortLabel>
                                        </TableCell>
                                    );
                                })}
                                {/* Conditionally render the "Actions" column */}
                                {buttonGroup && (
                                    <TableCell
                                        align="center"
                                        sx={{
                                            fontWeight: 'bold',
                                            fontSize: '17px', // Set column name size size
                                            backgroundColor: 'black',
                                        }}>
                                        Actions
                                    </TableCell>
                                )}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.length > 0 ? (
                                data
                                    .sort(getComparator(order, orderBy))
                                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                                    .map((row) => {
                                        return (
                                            <TableRow
                                                hover
                                                role="checkbox"
                                                tabIndex={-1}
                                                key={row.job_id}
                                            >
                                                {columns.map((column) => {
                                                    // Table body contents
                                                    let value = row[column];
                                                    if (column === "user_id" || column === "parameters") {
                                                        return null;
                                                    }

                                                    if (column === "created_timestamp" || column === "last_updated_timestamp") {
                                                        const formattedTimestamp = new Date(value).toLocaleString(undefined, { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
                                                        const [datePart, timePart] = formattedTimestamp.split(','); // Split date and time parts
                                                        return (
                                                            <TableCell key={`${row.job_id}-${column}`}>
                                                                {datePart.trim()} {/* Display date */}
                                                                {timePart.trim()} {/* Display time */}
                                                            </TableCell>);
                                                    }

                                                    if (column == "job_status") {
                                                        return (
                                                            <TableCell key={`${row.job_id}-${column}`}>
                                                                {renderStatus(value)}
                                                            </TableCell>
                                                        )
                                                    }

                                                    // For rows that do not require additional handling
                                                    return (
                                                        <TableCell key={`${row.job_id}-${column}`} align="left">
                                                            {column === "job_id" ? (
                                                                showJobIds ? value : <IconButton onClick={toggleShowJobIds}><VisibilityIcon /></IconButton>
                                                            ) : value}
                                                        </TableCell>
                                                    );
                                                })}
                                                {/* Conditionally render the "Actions" column */}
                                                {buttonGroup && (
                                                    <TableCell align="left" key={`actions-${row.job_id}`}>
                                                        {/* Pass the job status for the current row as a prop */}
                                                        {React.cloneElement(buttonGroup,
                                                            {
                                                                key: `actions-${row.job_id}`,
                                                                jobStatus: row.job_status,
                                                                jobId: row.job_id
                                                            })}
                                                    </TableCell>
                                                )}
                                            </TableRow>
                                        );
                                    })
                            ) : (
                                // Render a row with a cell that spans all columns if data is empty
                                <TableRow key="no-jobs-row">
                                    <TableCell colSpan={columns.length} align="center">
                                        <Typography>No jobs found</Typography>
                                    </TableCell>
                                </TableRow>
                            )}
                            <TableRow>
                                <TablePagination
                                    rowsPerPageOptions={[5, 10, 25]}
                                    count={data.length}
                                    rowsPerPage={rowsPerPage}
                                    page={page}
                                    onPageChange={handleChangePage}
                                    onRowsPerPageChange={handleChangeRowsPerPage}
                                />
                            </TableRow>
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>
        </>
    );
};

export default GenericJobTable;
