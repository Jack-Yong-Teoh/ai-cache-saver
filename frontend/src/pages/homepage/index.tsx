import React from "react";

const HonmePage: React.FC = () => {
  return (
    <div className={`homepage__container`}>
      {/* display purpose only, do not use html tag directly other than div */}
      <h1 className={`homepage__container__title`}>{"Hello World :)"}</h1>
    </div>
  );
};

export default HonmePage;
