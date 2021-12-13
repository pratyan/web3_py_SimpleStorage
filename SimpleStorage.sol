pragma solidity ^0.6.0;

contract SimpleStorage {
    //this will get initialized to 0
    //the public keyword will declare the visibility of the varibale
    uint256 public favoriteNumber;

    //Structure
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    //creating a object named 'person' of 'People' type
    People public person = People({favoriteNumber:2, name:"Pratyan majumder"});

    //creating a array of type 'People'
    // its a dynamic array cause its length is not defined
    People[] public people;
  
    //mapping
    mapping(string => uint256) public nameToFavoriteNumber;

    // bool favoriteBool = false;
    // string favoriteString = "String";
    // int256 favoriteInt = -5;
    // address favoriteAddress = 0x9E7D972391e460B1856576D91644d1c3Bd46a0bE;
    // bytes32 favoriteBytes = "cat";

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
        // uint256 test = 4;
    }

    //view keyword give access to only view the content of the fuction
    function retrive() public view returns(uint256){
        return favoriteNumber;
    }

    //pure keyword stands for if any mathematical is happening
    function doMath(uint256 _favoriteNumber) public pure{
        _favoriteNumber+_favoriteNumber;
    }

    //function to add person in array 'people' of type 'People'
    //'memory' stores only upto the execution, whereas 'storage' is more permanent
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        //to add elements into array into array, 'array.push(ele)'
        people.push(People({favoriteNumber:_favoriteNumber, name:_name}));

        //mapping
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }



}