import {Typography, Container, Divider} from "@mui/material";
import TypingAnimation from "../../components/common/Animations/TypingAnimation";
import ImageCardsGrid from "../../components/common/Cards/ImageCardsGrid";

const HomePage = () => {
  const cardDetails = [
    { imageUrl: "src/assets/images/img1.webp", title: "About Us", description: "Requirements 2 Design aims to streamline development by converting requirements to design" },
    { imageUrl: "src/assets/images/img2.webp", title: "Our Work", description: "See what we've done" },
    { imageUrl: "src/assets/images/img3.webp", title: "Our Values", description: "Understand our core values" },
    { imageUrl: "src/assets/images/img4.webp", title: "Contact Us", description: "Get in touch with us" },
    { imageUrl: "src/assets/images/img5.webp", title: "Showcase", description: "Start building" },
    { imageUrl: "src/assets/images/img6.webp", title: "Expedite Development", description: "See our projects" },
    { imageUrl: "src/assets/images/img7.webp", title: "Quick Design", description: "R2D helps with rapid design" },
    { imageUrl: "src/assets/images/img8.webp", title: "Requirements To Deisgn", description: "Easily convert your requirements to software design" },
  ];

  return (
    <Container>
      <div>
        <TypingAnimation text="Streamline Development" variant="h3"/>
      </div>
      <Divider sx={{ my: 2 }}></Divider>
      <Typography variant="h6" sx={{textAlign:'justify'}}>
        Discover our innovative platform designed to revolutionize the way you create software diagrams.  R2D helps you effortlessly model your business requirements into software architecture diagrams. Enabling rapid design, change, and solutions.
      </Typography>
      <Divider sx={{ my: 2 }}></Divider>
      <ImageCardsGrid cards={cardDetails} />
    </Container>
  );
}

export default HomePage;
