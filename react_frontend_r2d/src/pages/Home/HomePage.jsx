import {Typography} from "@mui/material";
import TypingAnimation from "../../components/common/Animations/TypingAnimation";
import CardsGrid from "../../components/common/Cards/ImageCardsGrid";

const HomePage = () => {
  const cardDetails = [
    { imageUrl: "src/assets/images/img1.webp", title: "About Us", description: "Requirements 2 Design aims to streamline development by converting requirements to design" },
    { imageUrl: "src/assets/images/img2.webp", title: "Our Work", description: "See what we've done" },
    { imageUrl: "src/assets/images/img3.webp", title: "Our Values", description: "Understand our core values" },
    { imageUrl: "src/assets/images/img4.webp", title: "Contact Us", description: "Get in touch with us" },
    { imageUrl: "src/assets/images/img4.webp", title: "Contact Us", description: "Get in touch with us" },
    { imageUrl: "src/assets/images/img4.webp", title: "Contact Us", description: "Get in touch with us" },
    { imageUrl: "src/assets/images/img4.webp", title: "Contact Us", description: "Get in touch with us" },
    { imageUrl: "src/assets/images/img4.webp", title: "Contact Us", description: "Get in touch with us" },
  ];

  return (
    <>
      <Typography>
        <TypingAnimation text="Streamline Development" variant="h3"/>
      </Typography>
      <hr></hr>
      <Typography variant="h6" sx={{textAlign:'justify'}}>
        Discover our innovative platform designed to revolutionize the way you create software diagrams.  R2D helps you can effortlessly transform requirements into detailed diagrams, accelerating the development process and enhancing collaboration. Experience a seamless transition from concept to visualization, ensuring your projects are not just completed faster but with precision you can count on.
      </Typography>
      <hr></hr>
      <CardsGrid cards={cardDetails} />
    </>
  );
}

export default HomePage;
