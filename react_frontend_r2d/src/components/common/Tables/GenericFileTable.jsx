import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TablePagination, TableSortLabel, Typography, Dialog, DialogTitle, DialogActions, DialogContent, Button, Box } from '@mui/material';
import ReadOnlyEditor from './ReadOnlyEditor';
import FileReaderUtility from '../../../utils/FileReaders/FileReaderUtility';


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
*/
const GenericFileTable = ({ repository }) => {
  const [order, setOrder] = useState('asc');
  const [orderBy, setOrderBy] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [data, setData] = useState([]);
  const [columns, setColumns] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [fileContent, setFileContent] = useState('');
  const [fileMetadata, setFileMetadata] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      const response = await repository.handleReadAllFiles();
      if (response.success) {
        setData(response.data); 
      } else {
        alert('Failed to fetch data');
      }
    };
  
    fetchData();
  }, [repository]); 
  
  useEffect(() => {
    if (data.length > 0) {
      const columnNames = Object.keys(data[0]).filter(key => key !== "content"); // Assuming you want to exclude 'content' from columns
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
      alert('Failed to fetch data');
    }
  };

  const handleCloseDialog = () => {
      setOpenDialog(false);
      setFileContent('');
  };

  const emptyRows = rowsPerPage - Math.min(rowsPerPage, data.length - page * rowsPerPage);

  return (
    <>
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column}
                  align="center"
                  sortDirection={orderBy === column ? order : false}
                >
                  <TableSortLabel
                    active={orderBy === column}
                    direction={orderBy === column ? order : 'asc'}
                    onClick={(event) => handleRequestSort(event, column)}
                  >
                    {column}
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
                          const value = row[column];
                          return (
                            <TableCell key={column} align="center">
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
              {emptyRows > 0 && data.length > 0 && (
                <TableRow style={{ height: 53 * emptyRows }}>
                  <TableCell colSpan={columns.length} />
                </TableRow>
              )}
        </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={data.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
     </Paper>
     {/* Dialog for displaying file content */}
     <Dialog open={openDialog} onClose={handleCloseDialog} aria-labelledby="file-content-title">
      <DialogTitle id="file-content-title">{}</DialogTitle>
      <DialogContent>
          <Box sx = {{width:"30vw", height:"50vh"}}>
          <Typography variant="h6">{fileMetadata.filename}</Typography>
          <hr></hr>
          <ReadOnlyEditor fileExtension={fileMetadata.type} fileContents={fileContent}></ReadOnlyEditor>
          <hr></hr>
          </Box>
      </DialogContent>
      <DialogActions>
          <Button onClick={handleCloseDialog}>Close</Button>
      </DialogActions>
     </Dialog>
 </>
  );
};

export default GenericFileTable;
