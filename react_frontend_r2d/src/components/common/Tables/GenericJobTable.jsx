import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TablePagination, TableSortLabel, Typography, IconButton, Chip, CircularProgress, Tooltip } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useAlert } from '../Alerts/AlertContext';

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


/*
* Displays a Table with pagination and sorting by columns.
* The table retrieves its data from the indexedDb datastore specified by the repository.
* Expects the table to store a column for File data types
**/

const GenericJobTable = ({ repository, buttonGroup = null }) => {
    const [order, setOrder] = useState('asc');
    const [orderBy, setOrderBy] = useState('');
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const [data, setData] = useState([]);
    const [columns, setColumns] = useState([]);
    const [openDialog, setOpenDialog] = useState(false);
    const { showAlert } = useAlert();

    const [showJobIds, setShowJobIds] = useState(false); // State to track visibility of job IDs

    useEffect(() => {
        const fetchData = async () => {
            const response = await repository.handleReadAll();
            if (response.success) {
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

    const handleOpenDialog = async (id) => {
        // This logic should be for search icon button
        setOpenDialog(true);
        const response = await repository.handleFindById(id);
        console.debug(response);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);

    };

    // When visibility icon is clicked job ids are shown
    const toggleShowJobIds = () => {
        setShowJobIds(!showJobIds);
    };

    // Render status as chips.
    // Add an indefinite spinner for processing status
    const renderStatus = (status) => {
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
                        <Chip label={status} color='error'/>
                    </Tooltip>
                );
            case "Error Failed to Process":
                return (
                    <Tooltip title="Errors were encountered while processing your request.
                    Verify that your job parameters are valid, and resubmit again.">
                        <Chip label={status} color='error'/>
                    </Tooltip>
                );
            case "Completed":
                return (
                    <Tooltip title="Your request has been completed successfully.">
                        <Chip label={status} color='success'/>
                    </Tooltip>
                );
            case "Processing":
                return (
                    <Tooltip title="Your request is currently being processed. Please wait while we generate your diagrams.">
                        <Chip
                            label="Processing"
                            icon={<CircularProgress size={18} color="inherit" />}
                            color='primary'
                            variant='outlined'
                        />
                    </Tooltip>
                );
            default:
                return null;
        }
    };
    return (
        <>
            <Paper elevation={0} sx={{
                border: '1px solid #90caf9',
            }}>
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
                                            sortDirection={orderBy === column ? order : true}
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
                                                onClick={() => handleOpenDialog(row.job_id)}>
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
                                                            <TableCell>
                                                                {datePart.trim()} {/* Display date */}
                                                                {timePart.trim()} {/* Display time */}
                                                            </TableCell>);
                                                    }
                                                    
                                                    if (column == "job_status") {
                                                        return (
                                                            <TableCell>
                                                            {renderStatus(value)}
                                                            </TableCell>
                                                            
                                                        )
                                                    }

                                                    // For rows that do not require additional handling
                                                    return (
                                                        <TableCell key={column} align="left">
                                                            {column === "job_id" ? (
                                                                showJobIds ? value : <IconButton onClick={toggleShowJobIds}><VisibilityIcon /></IconButton>
                                                            ) : value}
                                                        </TableCell>
                                                    );
                                                })}
                                                {/* Conditionally render the "Actions" column */}
                                                {buttonGroup && (
                                                    <TableCell align="left">
                                                        {/* Pass the job status for the current row as a prop */}
                                                        {React.cloneElement(buttonGroup, { jobStatus: row.job_status })}
                                                    </TableCell>
                                                )}
                                            </TableRow>
                                        );
                                    })
                            ) : (
                                // Render a row with a cell that spans all columns if data is empty
                                <TableRow>
                                    <TableCell colSpan={columns.length} align="center">
                                        <Typography>Table is Empty</Typography>
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
