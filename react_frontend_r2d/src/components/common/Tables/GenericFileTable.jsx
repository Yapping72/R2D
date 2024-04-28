import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TablePagination, TableSortLabel, Typography, Chip, Tooltip, Container } from '@mui/material';
import FileReaderUtility from '../../../utils/FileHandling/FileReaderUtility';
import FileContentDialog from '../Dialog/FileContentDialog';
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
const GenericFileTable = ({ repository, handleFileSelection, actions = [] }) => {
  const [order, setOrder] = useState('asc');
  const [orderBy, setOrderBy] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [data, setData] = useState([]);
  const [columns, setColumns] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [fileContent, setFileContent] = useState('');
  const [fileMetadata, setFileMetadata] = useState('');
  const { showAlert } = useAlert();

  useEffect(() => {
    const fetchData = async () => {
      const response = await repository.handleReadAllFiles();
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
    setOpenDialog(true);
    const response = await repository.handleFindById(id);
    if (response.success) {
      const fileContent = await FileReaderUtility.readAsText(response.data.content);
      setFileContent(fileContent)
      await setFileMetadata(response.data)
    } else {
      showAlert('error', `We're having trouble displaying your file contents. Please try again later.`)
    }
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setFileContent('');
  };

  const truncateLabel = (label) => {
    const maxCharLimit = 20; // Maximum character limit for chip labels
    let words = label.split(" "); // Split label into words
    let truncatedLabel = "";
    let currentLength = 0;
    let wordCount = 0;
  
    for (let word of words) {
      // Check the length with the next word added
      if (currentLength + word.length + (truncatedLabel ? 1 : 0) > maxCharLimit) {
        // If adding this word exceeds the limit and more than one word has been added, stop
        truncatedLabel += (truncatedLabel ? " " : "") + word;
        break;
      }
      // Add the word to the result (add a space before the word if it's not the first word)
      truncatedLabel += (truncatedLabel ? " " : "") + word;
      currentLength += word.length + (truncatedLabel ? 1 : 0); // Update the current length including space
      wordCount++;
    }
  
    // If the final string is shorter than the original and more words exist, add ellipsis
    if (currentLength < label.length) {
      truncatedLabel += '...';
    }
    return truncatedLabel;
  };

  
  const renderArrayContentAsChips = (value, chipColor="secondary") => {
    const numberOfChipsToShow = 3; // Number of chips to display
    if (value.length > numberOfChipsToShow) {
      const visibleChips = value.slice(0, numberOfChipsToShow);
      const moreCount = value.length - numberOfChipsToShow;
      return (

        <TableCell>
          {visibleChips.map((item, index) => (
            <Tooltip title={value.join(', ')}>
            <Chip key={index} color={chipColor} label={truncateLabel(item)} style={{ margin: '2px' }} variant='outlined' />
            </Tooltip>
          ))}
          <Tooltip title={value.splice(numberOfChipsToShow).join(', ')}>
            <Chip label={`+${moreCount} more`} style={{ margin: '2px'}} variant='outlined' />
            </Tooltip>
        </TableCell>
  
      );
    }

    return (

      <TableCell>
        <Tooltip title={value.join(', ')}>
        {value.map((item, index) => (
          <Chip key={index} color={chipColor} label={truncateLabel(item)}  style={{ margin: '2px' }} variant='outlined' />
        ))}
        </Tooltip>
      </TableCell>

    );
  }

  return (
    <>
      <Paper elevation={0} sx={{
        border: '1px solid #90caf9',
      }}>
        <TableContainer sx={{ maxHeight: '100%' }}>
        <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                {columns.map((column) => (
                  <TableCell
                    key={column}
                    align="left"
                    sortDirection={orderBy === column ? order : false}
                    sx={{
                      fontWeight: 'bold',
                      fontSize: '18px', // Set column name size
                      backgroundColor:'black',
                    }}
                  >
                    <TableSortLabel
                      active={orderBy === column}
                      direction={orderBy === column ? order : 'desc'}
                      onClick={(event) => handleRequestSort(event, column)}
                    >
                      {column.charAt(0).toUpperCase() + column.slice(1)}
                    </TableSortLabel>
                  </TableCell>
                ))}
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
                        key={row.id}
                        onClick={() => handleOpenDialog(row.id)}>
                        {columns.map((column) => {
                          let value = row[column];
                          // Check if the column is 'features' or 'sub features' and the value is a Set or List
                          if ((column === "features" || column === "sub features") && (Array.isArray(value) || value instanceof Set)) {
                            value = Array.from(value); // Ensure value is an array
                            const chipColor = (column === "features") ? "primary" : "secondary";
                            return (
                              renderArrayContentAsChips(value, chipColor)
                            ); 
                          }
                          return (
                            <TableCell key={column} align="left">
                              {value}
                            </TableCell>
                          );
                        })}
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

        {/* Dialog for displaying file content on click*/}
        <FileContentDialog
          open={openDialog}
          onClose={handleCloseDialog}
          fileContent={fileContent}
          fileMetadata={fileMetadata}
          handleFileSelection={handleFileSelection}
        />
      </Paper>
    </>
  );
};

export default GenericFileTable;
